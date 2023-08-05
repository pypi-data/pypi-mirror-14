# -*- coding: utf-8 -*-
from exceptions import AlaudaInputError, AlaudaServerError
import json
import time
from string import Template
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

VOLUME_MIN_SIZE = 10
VOLUME_MAX_SIZE = 100


def parse_image_name_tag(image):
    result = image.split(':')
    if len(result) == 1:
        return image, 'latest'
    elif len(result) == 2:
        return result[0], result[1]
    else:
        raise AlaudaInputError('Invalid image name')


def parse_target_state(start):
    if start:
        return 'STARTED'
    else:
        return 'STOPPED'


def parse_instance_ports(port_list):
    def _parse_instance_port(_port):
        result = _port.split('/')
        if len(result) > 2:
            raise AlaudaInputError('Invalid port description. (Example of valid description: 80/tcp)')

        try:
            if len(result) == 1 and _port.find(':') > -1:
                result = _port.split(':')
                result = [result[0]]
            port = int(result[0])
        except:
            raise AlaudaInputError('Invalid port description. (Example of valid description: 80/tcp)')

        if len(result) == 2:
            protocol = result[1]
        else:
            if port == 80:
                protocol = 'http'
            else:
                protocol = 'tcp'

        if protocol not in ['tcp', 'http', 'internal']:
            raise AlaudaInputError('Invalid port protocal. Supported protocols: {tcp}')
        if port < 0 or port > 65535:
            raise AlaudaInputError('Invalid port number')

        return port, 'tcp', protocol

    parsed_ports = []
    ports = []
    if port_list is not None:
        for port_desc in port_list:
            port, protocol, port_type = _parse_instance_port(port_desc)
            result = {"container_port": port, "protocol": 'tcp', 'endpoint_type': '{}-endpoint'.format(port_type)}
            if result not in parsed_ports:
                parsed_ports.append(result)
                ports.append(port)
    return parsed_ports, ports


def merge_internal_external_ports(ports, exposes):
    expose_list = []
    if exposes is None:
        return expose_list
    for expose in exposes:
        if not str(expose).isdigit() or int(expose) < 0 or int(expose) > 65535:
            raise AlaudaInputError('Invalid port number')
        expose = int(expose)
        if expose in ports:
            continue
        result = {"container_port": expose, "protocol": 'tcp', 'endpoint_type': 'internal-endpoint'}
        if result not in expose_list:
            expose_list.append(result)
    return expose_list


def parse_envvar(_envvar):
    def _parse_envvar_dict(_envvar):
        if len(_envvar) != 1:
            raise AlaudaInputError('Invalid environment variable. (Example of valid description: FOO=foo)')
        key = _envvar.keys()[0]
        value = _envvar[key]
        if value is None:
            value = ''
        return key, str(value)

    def _parse_envvar_str(_envvar):
        pos = _envvar.find('=')
        if pos != -1:
            key = _envvar[:pos]
            value = _envvar[pos + 1:]
            return key, value
        else:
            pos = _envvar.find(':')
            if pos == -1:
                raise AlaudaInputError('Invalid environment variable. (Example of valid description: FOO=foo)')
            key = _envvar[:pos]
            value = _envvar[pos + 1:]
            return key, value

    if isinstance(_envvar, dict):
        return _parse_envvar_dict(_envvar)
    elif isinstance(_envvar, str):
        return _parse_envvar_str(_envvar)
    else:
        raise AlaudaInputError('Invalid environment variable. (Example of valid description: FOO=foo)')


def parse_envvars(envvar_list):
    parsed_envvars = {}
    if envvar_list is not None:
        for envvar in envvar_list:
            key, value = parse_envvar(envvar)
            parsed_envvars[key] = value
    return parsed_envvars


def parse_volume(_volume):
    if not isinstance(_volume, str):
        raise AlaudaInputError('Invalid volume description. (Example of valid description: /var/lib/data1:10:[backup_id])')
    result = _volume.split(':')
    if len(result) == 1:
        result.append('10')
    if len(result) != 2 and len(result) != 3:
        raise AlaudaInputError('Invalid volume description. (Example of valid description: /var/lib/data1:10:[backup_id])')

    path = result[0]
    try:
        size = int(result[1])
        if size < VOLUME_MIN_SIZE or size > VOLUME_MAX_SIZE:
            raise AlaudaInputError(
                'Invalid volume size {0}. Volume size must be between {1} and {2}'.format(
                    size,
                    VOLUME_MIN_SIZE,
                    VOLUME_MAX_SIZE))
        backup_id = None
        if len(result) == 3:
            backup_id = result[2]
    except AlaudaInputError as ex:
        raise ex
    except:
        print "except"
        raise AlaudaInputError('Invalid volume description. (Example of valid description: /var/lib/data1:10:[backup_id])')
    return path, size, backup_id


def parse_volumes(volume_list):
    parsed_volumes = []
    if volume_list is not None:
        for volume_desc in volume_list:
            path, size, backup_id = parse_volume(volume_desc)
            volume = {"app_volume_dir": path, "size_gb": size, "volume_type": "EBS"}
            if backup_id is not None:
                volume['backup_id'] = backup_id
            parsed_volumes.append(volume)
    return parsed_volumes


def parse_links(link_list):
    def _parse_link(_link):
        if not isinstance(_link, str):
            raise AlaudaInputError('Invalid link description. (Example of valid description: mysql:db)')
        result = _link.split(':')
        if len(result) > 2:
            raise AlaudaInputError('Invalid link description. (Example of valid description: mysql:db)')
        if len(result) == 1 or len(result[1]) == 0:
            return result[0], result[0]
        return result[0], result[1]

    parsed_links = []
    if link_list is not None:
        for link in link_list:
            service_name, alias = _parse_link(link)
            parsed_links.append((service_name, alias))
    return parsed_links


def parse_scale(name_number_list):
    def _parse_scale(_name_number):
        result = _name_number.split('=')
        if len(result) != 2:
            raise AlaudaInputError('Invalid scale description. (Example of valid description: mysql=3)')

        name = result[0]
        try:
            number = int(result[1])
        except:
            raise AlaudaInputError('Invalid scale description. (Example of valid description: mysql=3)')
        return name, number

    scale_dict = {}
    for name_number in name_number_list:
        name, number = _parse_scale(name_number)
        scale_dict[name] = number
    return scale_dict


def parse_autoscale_info(info):
    if info is None:
        return 'MANUAL', {}
    mode = info[0]
    cfg_file = info[1]
    if mode:
        try:
            fp = file(cfg_file)
        except:
            raise AlaudaInputError('can not open auto-scaling config file-> {}.'.format(cfg_file))
        try:
            cfg_json = json.load(fp)
            fp.close()
        except:
            fp.close()
            raise AlaudaInputError('Parse {} fail! The format refer to ./auto-scaling.cfg'.format(cfg_file))
        return 'AUTO', json.dumps(cfg_json)
    else:
        return 'MANUAL', {}


def parse_date(start_date, end_date):
    if start_date is None:
        raise AlaudaInputError('Please spec start date')
    if end_date is None:
        end_date = start_date
    if start_date > end_date:
        raise AlaudaInputError('start date is early than end date')
    start = int(time.mktime(time.strptime(start_date, '%Y%m%d')))
    end = int(time.mktime(time.strptime(end_date, '%Y%m%d')))
    date_list = []
    while start <= end:
        date_list.append(time.strftime('%Y%m%d', time.localtime(start)))
        start += 24 * 3600
    return date_list


def parse_time(start_time, end_time):
    if start_time is not None and end_time is not None:
        try:
            start = time.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            end = time.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            start = int(time.mktime(start))
            end = int(time.mktime(end))
            return start, end
        except:
            raise AlaudaInputError('Please make sure time format like 2015-05-01 12:00:00')
    elif start_time is None and end_time is None:
        end = int(time.time())
        start = end - 900
    elif start_time is not None:
        start = time.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        start = int(time.mktime(start))
        end = int(time.time())
    else:
        end = time.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        end = int(time.mktime(end))
        start = end - 900
    return start, end


def failed(status_code):
    return status_code < 200 or status_code >= 300


def check_response(response):
    if failed(response.status_code):
        raise AlaudaServerError(response.status_code, response.text)


def expand_environment(envvars):
    for key, value in envvars.items():
        expanded = Template(value).safe_substitute(envvars)
        envvars[key] = expanded


def print_ports(service):
    max_type_len = len('Type')
    max_container_port_len = len('Container_port')
    max_service_port_len = len('Service_port')
    max_ip_len = len('Ip')

    data = json.loads(service.details)
    status = data['current_status']
    if status != 'Running':
        print '{} is not in Running state.Please wait or start it!'.format(data['service_name'])
        return
    instance_ports = data.get('instance_ports')
    instances = data.get('instances')
    for instance_port in instance_ports:
        if max_type_len < len(instance_port.get('endpoint_type')):
            max_type_len = len((instance_port.get('endpoint_type')))
        if max_ip_len < len(instance_port.get('ipaddress')):
            max_ip_len = len(instance_port.get('ipaddress'))
    if max_type_len < len('direct_endpoint'):
        max_type_len = len('direct_endpoint')
    print '{0}    {1}    {2}    {3}'.format('Type'.center(max_type_len),
                                            'Service_port'.center(max_service_port_len),
                                            'Container_port'.center(max_container_port_len),
                                            'Ip'.center(max_ip_len))
    print '{0}'.format('-' * (max_type_len + max_container_port_len + max_service_port_len + max_ip_len + 3 * 4))
    for instance_port in instance_ports:
        print'{0}    {1}    {2}    {3}'.format(str(instance_port.get('endpoint_type')).ljust(max_type_len),
                                               str(instance_port.get('service_port')).ljust(max_service_port_len),
                                               str(instance_port.get('container_port')).ljust(max_container_port_len),
                                               str(instance_port.get('ipaddress')).ljust(max_ip_len))
    for instance in instances:
        instance_ports = instance.get('instance_ports')
        for instance_port in instance_ports:
            if instance_port.get('service_port', None) is not None:
                print '{0}    {1}    {2}    {3}'.format('direct_endpoint'.ljust(max_type_len),
                                                        str(instance_port.get('service_port')).ljust(max_service_port_len),
                                                        str(instance_port.get('container_port')).ljust(max_container_port_len),
                                                        '')


def print_app_output(service_list):
    def _get_run_command(data):
        run_command = data['run_command']
        if not run_command:
            run_command = ' '
        return run_command

    max_name_len = len('Name')
    max_command_len = len('Command')
    max_state_len = len('State')
    max_instance_count_len = len('Instance Count')
    max_link_len = len('Link')

    for service in service_list:
        if max_name_len < len(service['service_name']):
            max_name_len = len(service['service_name'])
        run_command = _get_run_command(service)
        if max_command_len < len(run_command):
            max_command_len = len(run_command)
        if max_state_len < len(service['current_status']):
            max_state_len = len(service['current_status'])
        if max_instance_count_len < len(str(service['target_num_instances'])):
            max_instance_count_len = len(str(service['target_num_instances']))
        if max_link_len < len(service['linked_to_apps']):
            max_link_len = len(service['linked_to_apps'])
    print '{0}    {1}    {2}    {3}    {4}'.format('Name'.center(max_name_len), 'Command'.center(max_command_len), 'State'.center(max_state_len),
                                                   'Instance Count'.center(max_instance_count_len),
                                                   'Link'.center(max_link_len))
    print '{0}'.format('-' * (max_name_len + max_command_len + max_state_len + max_instance_count_len + max_link_len + 4 * 4))
    for service in service_list:
        print '{0}    {1}    {2}    {3}    {4}'.format(service['service_name'].ljust(max_name_len), _get_run_command(service).ljust(max_command_len),
                                                       service['current_status'].ljust(max_state_len),
                                                       str(service['target_num_instances']).ljust(max_instance_count_len),
                                                       str(service['linked_to_apps']).ljust(max_link_len))


def print_ps_output(service_list):
    max_name_len = len('Name')
    max_command_len = len('Command')
    max_state_len = len('State')
    max_ports_len = len('Ports')
    max_instance_count_len = len('Instance Count')
    max_iaas_len = len('IaaS')
    max_region_len = len('Region')

    for service in service_list:
        if max_name_len < len(service.name):
            max_name_len = len(service.name)
        run_command = service.get_run_command()
        if max_command_len < len(run_command):
            max_command_len = len(run_command)
        state = service.get_state()
        if max_state_len < len(state):
            max_state_len = len(state)
        ports = service.get_ports()
        if max_ports_len < len(ports):
            max_ports_len = len(ports)
        if max_instance_count_len < len(str(service.target_num_instances)):
            max_instance_count_len = len(str(service.target_num_instances))
        iaas, region_name = service.get_region_info()
        if max_iaas_len < len(iaas):
            max_iaas_len = len(iaas)
        if max_region_len < len(region_name):
            max_region_len = len(region_name)

    print '{0}    {1}    {2}    {3}    {4}    {5}    {6}'.format('Name'.center(max_name_len), 'Command'.center(max_command_len), 'State'.center(max_state_len),
                                                                 'Ports'.center(max_ports_len), 'Instance Count'.center(max_instance_count_len),
                                                                 'IaaS'.center(max_iaas_len), 'Region'.center(max_region_len))
    print '{0}'.format('-' * (max_name_len + max_command_len + max_state_len + max_ports_len + max_instance_count_len + max_iaas_len + max_region_len + 6 * 4))
    for service in service_list:
        iaas, region_name = service.get_region_info()
        print '{0}    {1}    {2}    {3}    {4}    {5}    {6}'.format(service.name.ljust(max_name_len), service.get_run_command().ljust(max_command_len),
                                                                     service.get_state().ljust(max_state_len), service.get_ports().ljust(max_ports_len),
                                                                     str(service.target_num_instances).ljust(max_instance_count_len),
                                                                     str(iaas).ljust(max_iaas_len), str(region_name).ljust(max_region_len))


def print_backup_ps_output(backup_list):
    max_name_len = len('Name')
    max_id_len = len('Id')
    max_state_len = len('State')
    max_time_len = len('Created time')
    max_size_len = len('Size')

    for data in backup_list:
        backup = json.loads(data.details)
        if max_name_len < len(backup['name']):
            max_name_len = len(backup['name'])
        if max_id_len < len(backup['backup_id']):
            max_id_len = len(backup['backup_id'])
        if max_state_len < len(backup['status']):
            max_state_len = len(backup['status'])
        if max_time_len < len(backup['created_datetime']):
            max_time_len = len(backup['created_datetime'])
        size_byte = backup.get('size_byte', ' ')
        if max_size_len < len(str(size_byte)):
            max_size_len = len(str(size_byte))

    print '{0}    {1}    {2}    {3}    {4}'.format('Id'.center(max_id_len), 'Name'.center(max_name_len), 'State'.center(max_state_len),
                                                   'Size'.center(max_size_len), 'Created time'.center(max_time_len))
    print '{0}'.format('-' * (max_id_len + max_name_len + max_state_len + max_time_len + max_size_len + 4 * 4))

    for data in backup_list:
        backup = json.loads(data.details)
        print '{0}    {1}    {2}    {3}    {4}'.format(str(backup['backup_id']).ljust(max_id_len), str(backup['name']).ljust(max_name_len),
                                                       str(backup['status']).ljust(max_state_len), str(backup.get('size_byte', ' ')).ljust(max_size_len),
                                                       str(backup['created_datetime']).ljust(max_time_len))


def print_instance_ps_output(instance_list):
    max_name_len = len('Name')
    max_id_len = len('ID')
    max_time_len = len('Created time')

    for data in instance_list:
        instance = json.loads(data.details)
        if max_name_len < len(instance['instance_name']):
            max_name_len = len(instance['instance_name'])
        if max_id_len < len(instance['uuid']):
            max_id_len = len(instance['uuid'])
        if max_time_len < len(instance['started_at']):
            max_time_len = len(instance['started_at'])

    print '{0}    {1}    {2}'.format('Name'.center(max_name_len), 'ID'.center(max_id_len), 'Created time'.center(max_time_len))
    print '{0}'.format('-' * (max_name_len + max_id_len + max_time_len + 4 * 2))

    for data in instance_list:
        instance = json.loads(data.details)
        print '{0}    {1}    {2}'.format(str(instance['instance_name']).ljust(max_name_len), str(instance['uuid']).ljust(max_id_len),
                                         str(instance['started_at']).ljust(max_time_len))


def print_organization_ps_output(orgs):
    max_name_len = len('Name')
    max_company_len = len('Company')
    max_time_len = len('Created time')

    for data in orgs:
        org = json.loads(data.details)
        org['company'] = str(org['company']).encode('GBK')
        if max_name_len < len(org['name']):
            max_name_len = len(org['name'])
        if max_time_len < len(org['created_at']):
            max_time_len = len(org['created_at'])
        if max_company_len < len(org['company']):
            max_company_len = len(org['company'])

    print '{0}    {1}    {2}'.format('Name'.center(max_name_len), 'Company'.center(max_company_len), 'Created time'.center(max_time_len))
    print '{0}'.format('-' * (max_name_len + max_company_len + max_time_len + 4 * 2))

    for data in orgs:
        org = json.loads(data.details)
        print '{0}    {1}    {2}'.format(str(org['name']).ljust(max_name_len), str(org['company']).ljust(max_company_len),
                                         str(org['created_at']).ljust(max_time_len))


def print_logs(logs, type, print_flag=True):
    entry_list = json.loads(logs.encode('utf-8'))
    if print_flag:
        print '[alauda] Logs:'
    if type == 'service':
        for entry in entry_list:
            print '{}\t{}\t{}'.format(entry['time'], entry['instance_id'], entry['message'])
    else:
        for entry in entry_list:
            print entry['message']


def print_json_result(result):
    try:
        print '[alauda] ' + json.dumps(json.loads(result), indent=2)
    except:
        print '[alauda] EMPTY'


def get_flag_pos(src, start_with, end_with, start_pos):
    start_with_pos = src.find(start_with, start_pos)
    if start_with_pos == -1:
        return -1, -1
    end_with_pos = src.find(end_with, start_with_pos + len(end_with))
    if end_with_pos == -1:
        end_with_pos = len(src)
    return start_with_pos, end_with_pos


def indegree0(v, e):
    if v == []:
        return None
    tmp = v[:]
    for i in e:
        if i[1] in tmp:
            tmp.remove(i[1])
    if tmp == []:
        return -1

    for t in tmp:
        for i in range(len(e)):
            if t in e[i]:
                e[i] = 'toDel'
    if e:
        eset = set(e)
        eset.remove('toDel')
        e[:] = list(eset)
    if v:
        for t in tmp:
            v.remove(t)
    return tmp


def topoSort(v, e):
    result = []
    while True:
        nodes = indegree0(v, e)
        if nodes is None:
            break
        if nodes == -1:
            print('there\'s a circle.')
            return None
        result.append(nodes)
    return result
