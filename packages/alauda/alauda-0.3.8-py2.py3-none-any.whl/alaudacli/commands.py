import getpass
import json
import requests

import util
import auth
import compose
from service import Service
from backup import Backup
from organization import Organization
from build import Build
from execute import Executer
from application import Application


def login(username, password, cloud, endpoint):
    if not username:
        username = raw_input('Username: ')
    if not password:
        password = getpass.getpass()

    api_endpoint = endpoint
    if api_endpoint is None:
        api_endpoint = auth.get_api_endpoint(cloud)
    url = api_endpoint + 'generate-api-token/'
    payload = {'username': username, 'password': password}
    r = requests.post(url, payload)
    util.check_response(r)
    d = json.loads(r.text)
    token = d['token']
    auth.save_token(api_endpoint, token, username)
    print '[alauda] Successfully logged in as {}.'.format(username)


def logout():
    auth.delete_token()
    print '[alauda] Bye'


def service_create(image, name, start, target_num_instances, instance_size, run_command, entrypoint,
                   env, ports, exposes, volumes, links, namespace, scaling_info, custom_domain_name, region_name):
    image_name, image_tag = util.parse_image_name_tag(image)
    instance_ports, port_list = util.parse_instance_ports(ports)
    expose_list = util.merge_internal_external_ports(port_list, exposes)
    instance_ports.extend(expose_list)
    instance_envvars = util.parse_envvars(env)
    links = util.parse_links(links)
    volumes = util.parse_volumes(volumes)
    scaling_mode, scaling_cfg = util.parse_autoscale_info(scaling_info)
    if scaling_mode is None:
        scaling_mode = 'MANUAL'
    service = Service(name=name,
                      image_name=image_name,
                      image_tag=image_tag,
                      target_num_instances=target_num_instances,
                      instance_size=instance_size,
                      run_command=run_command,
                      entrypoint=entrypoint,
                      instance_ports=instance_ports,
                      instance_envvars=instance_envvars,
                      volumes=volumes,
                      links=links,
                      namespace=namespace,
                      scaling_mode=scaling_mode,
                      autoscaling_config=scaling_cfg,
                      custom_domain_name=custom_domain_name,
                      region_name=region_name)
    if start:
        service.run()
    else:
        service.create()


def service_update(name, image_tag, target_num_instances, instance_size, run_command,
                   entrypoint, env, ports, exposes, namespace, app):
    service = Service.fetch(name, namespace, app)
    instance_ports, port_list = util.parse_instance_ports(ports)
    expose_list = util.merge_internal_external_ports(port_list, exposes)
    instance_ports.extend(expose_list)
    instance_ports = None if len(instance_ports) == 0 else instance_ports
    instance_envvars = util.parse_envvars(env)
    instance_envvars = None if len(instance_envvars) == 0 else instance_envvars
    service.update(image_tag, target_num_instances, instance_size, run_command, entrypoint, instance_envvars, instance_ports)


def service_inspect(name, namespace, app):
    service = Service.fetch(name, namespace, app)
    result = service.inspect()
    util.print_json_result(result)


def service_start(name, namespace, app):
    service = Service.fetch(name, namespace, app)
    service.start()


def service_stop(name, namespace, app):
    service = Service.fetch(name, namespace, app)
    service.stop()


def service_rm(name, namespace, app):
    Service.remove(name, namespace, app)


def service_ps(namespace, page, app):
    service_list = Service.list(namespace, page, app)
    util.print_ps_output(service_list)


def service_scale(descriptor, namespace, app):
    scale_dict = util.parse_scale(descriptor)
    for service_name, service_num in scale_dict.items():
        service = Service.fetch(service_name, namespace, app)
        service.scale(service_num)


def service_enable_autoscaling(name, namespace, autoscaling_config, app):
    _, scaling_cfg = util.parse_autoscale_info(('AUTO', autoscaling_config))
    service = Service.fetch(name, namespace, app)
    service.enable_autoscaling(scaling_cfg)


def service_disable_autoscaling(name, namespace, target_num_instances, app):
    service = Service.fetch(name, namespace, app)
    service.disable_autoscaling(target_num_instances)


def service_logs(name, namespace, start_time, end_time, app, tail):
    service = Service.fetch(name, namespace, app)
    if tail:
        service.tail_logs()
    result = service.logs(start_time, end_time)
    util.print_logs(result, 'service')


def service_logs_download(name, namespace, list_date, start_date, end_date, path):
    service = Service.fetch(name, namespace)
    print 'list date: {}'.format(list_date)
    if list_date:
        service.list_logs_date()
    else:
        service.logs_download(start_date, end_date, path)


def service_ports(name, namespace, app):
    service = Service.fetch(name, namespace, app)
    util.print_ports(service)


def service_exec(name, namespace, command, *args):
    executer = Executer.fetch(name, namespace)
    executer.execute(command, *args)


def instance_ps(name, namespace, app):
    service = Service.fetch(name, namespace, app)
    instance_list = service.list_instances()
    util.print_instance_ps_output(instance_list)


def instance_inspect(name, uuid, namespace, app):
    service = Service.fetch(name, namespace, app)
    instance = service.get_instance(uuid)
    result = instance.inspect()
    util.print_json_result(result)


def instance_logs(name, uuid, namespace, start_time=None, end_time=None, app=None):
    service = Service.fetch(name, namespace, app)
    instance = service.get_instance(uuid)
    result = instance.logs(start_time, end_time)
    util.print_logs(result, 'instance')


def compose_up(file, strict, namespace, region, ignore):
    project = compose.load_project(file, namespace, region)
    if strict:
        project.strict_up(ignore)
    else:
        project.up(ignore)


def compose_ps(file, namespace):
    project = compose.load_project(file, namespace, None)
    project.ps(namespace)


def compose_start(file, strict, namespace):
    project = compose.load_project(file, namespace, None)
    if strict:
        project.strict_start()
    else:
        project.start()


def compose_stop(file, namespace):
    project = compose.load_project(file, namespace, None)
    project.stop()


def compose_restart(file, strict, namespace):
    project = compose.load_project(file, namespace, None)
    if strict:
        project.strict_restart()
    else:
        project.restart()


def compose_rm(file, namespace):
    project = compose.load_project(file, namespace, None)
    project.rm(namespace)


def compose_scale(descriptor, file, namespace):
    project = compose.load_project(file, namespace, None)
    scale_dict = util.parse_scale(descriptor)
    project.scale(scale_dict, namespace)


def backup_create(name, service_name, mounted_dir, namespace):
    service = Service.fetch(service_name, namespace)
    backup = Backup(service=service, name=name, mounted_dir=mounted_dir)
    backup.create()


def backup_list(namespace):
    backup_list = Backup.list(namespace)
    util.print_backup_ps_output(backup_list)


def backup_inspect(id, namespace):
    backup = Backup.fetch(id, namespace)
    result = backup.inspect()
    util.print_json_result(result)


def backup_rm(id, namespace):
    Backup.remove(id, namespace)


def organization_create(name, company):
    orgs = Organization(name=name, company=company)
    orgs.create()


def organization_list():
    orgs_list = Organization.list()
    util.print_organization_ps_output(orgs_list)


def organization_inspect(name):
    orgs = Organization.fetch(name)
    result = orgs.inspect()
    util.print_json_result(result)


def organization_update(name, company):
    orgs = Organization.fetch(name)
    orgs.update(company)


def build_create(repo_name, source, namespace, image_tag, commit_id):
    build = Build()
    build.create(repo_name, source, namespace, image_tag, commit_id)


def app_create(name, namespace, region, file):
    app = Application(name, region, file, namespace)
    app.create()


def app_run(name, namespace, region, file):
    app = Application(name, region, file, namespace)
    app.create()
    app.start()


def app_inspect(name, namespace):
    app = Application(name, namespace=namespace)
    services = app.get()
    util.print_app_output(services)


def app_start(name, namespace):
    app = Application(name, namespace=namespace)
    app.start()


def app_stop(name, namespace):
    app = Application(name, namespace=namespace)
    app.stop()


def app_rm(name, namespace):
    app = Application(name, namespace=namespace)
    app.remove()
