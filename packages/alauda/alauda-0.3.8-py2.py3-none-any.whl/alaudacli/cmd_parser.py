import argparse

from alaudacli import __version__


def parse_cmds(argv):
    parser = create_parser()
    args = parser.parse_args(argv)
    return args


def create_parser():
    parser = argparse.ArgumentParser(description="Alauda CLI", prog='alauda')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    subparsers = parser.add_subparsers(title="Alauda CLI commands", dest='cmd')
    _add_login_parser(subparsers)
    _add_logout_parser(subparsers)
    _add_service_parser(subparsers)
    _add_compose_parser(subparsers)
    _add_backups_parser(subparsers)
    _add_organization_parser(subparsers)
    _add_build_parser(subparsers)
    _add_application_parser(subparsers)
    return parser


def _add_login_parser(subparsers):
    login_parser = subparsers.add_parser('login', help='Alauda login', description='Alauda login')
    login_parser.add_argument('-u', '--username', help='Alauda username')
    login_parser.add_argument('-p', '--password', help='Alauda password')
    login_parser.add_argument('-c', '--cloud', help='Alauda Cloud to connect to', choices={'cn', 'io'}, default='cn')
    login_parser.add_argument('-e', '--endpoint', help='Alauda API endpoint to use')


def _add_logout_parser(subparsers):
    subparsers.add_parser('logout', help='Log out', description='Log out')


def _add_service_parser(subparsers):
    service_parser = subparsers.add_parser('service', help='Service operations', description='Service operations')
    service_subparsers = service_parser.add_subparsers(title='Alauda service commands', dest='subcmd')

    create_parser = service_subparsers.add_parser('create', help='Create a new service', description='Create a new service')
    create_parser.add_argument('name', help='Service name')
    create_parser.add_argument('image', help='Docker image used by the service')
    create_parser.add_argument('-t', '--target-num-instances', help='Target number of instances for the service', type=int, default=1)
    create_parser.add_argument('-s', '--instance-size', help='Service container size', choices=['XS', 'S', 'M', 'L', 'XL'], default='XS')
    create_parser.add_argument('-r', '--run-command', help='The command used to start the service containers', default='')
    create_parser.add_argument('-ep', '--entrypoint', help='The entrypint used to run the command', default='')
    create_parser.add_argument('-e', '--env', help='Environment variables, e.g. VAR=value', action='append')
    create_parser.add_argument('-l', '--link', help='which service to link.', action='append')
    create_parser.add_argument('-p', '--publish', help='Ports to publish, e.g. 5000/tcp', action='append')
    create_parser.add_argument('-ex', '--expose', help='Internal ports, e.g. 5000', action='append', type=int)
    create_parser.add_argument('-v', '--volume', help='Volumes, e.g. /var/lib/mysql:10', action='append')
    create_parser.add_argument('-n', '--namespace', help='Service namespace')
    create_parser.add_argument('-a', '--autoscale', help='Enable auto-scaling', action='store_true')
    create_parser.add_argument('-f', '--autoscaling-config', help='Auto-scaling config file name', default='./auto-scaling.cfg')
    create_parser.add_argument('-d', '--domain', help='Custom domain name', default='')
    create_parser.add_argument('-re', '--region', help='Region name')

    run_parser = service_subparsers.add_parser('run', help='Create and start a new service', description='Create and start a new service')
    run_parser.add_argument('name', help='Service name')
    run_parser.add_argument('image', help='Docker image used by the service')
    run_parser.add_argument('-t', '--target-num-instances', help='Target number of instances for the service', type=int, default=1)
    run_parser.add_argument('-s', '--instance-size', help='Service container size', choices=['XS', 'S', 'M', 'L', 'XL'], default='XS')
    run_parser.add_argument('-r', '--run-command', help='The command used to start the service containers', default='')
    run_parser.add_argument('-ep', '--entrypoint', help='The entrypint used to run the command', default='')
    run_parser.add_argument('-e', '--env', help='Environment variables, e.g. VAR=value', action='append')
    run_parser.add_argument('-l', '--link', help='which service to link.', action='append')
    run_parser.add_argument('-p', '--publish', help='Ports to publish, e.g. 5000/tcp', action='append')
    run_parser.add_argument('-ex', '--expose', help='Internal ports, e.g. 5000', action='append', type=int)
    run_parser.add_argument('-v', '--volume', help='volumes.e.g. /var/lib/mysql:10', action='append')
    run_parser.add_argument('-n', '--namespace', help='Service namespace')
    run_parser.add_argument('-a', '--autoscale', help='Enable auto-scaling', action='store_true')
    run_parser.add_argument('-f', '--autoscaling-config', help='Auto-scaling config file name', default='./auto-scaling.cfg')
    run_parser.add_argument('-d', '--domain', help='Custom domain name', default='')
    run_parser.add_argument('-re', '--region', help='Region name')

    update_parser = service_subparsers.add_parser('update', help='Update an exist service', description='Update an exist service')
    update_parser.add_argument('name', help='Service name')
    update_parser.add_argument('-tg', '--tag', help='image tag')
    update_parser.add_argument('-t', '--target-num-instances', help='Target number of instances for the service', type=int)
    update_parser.add_argument('-s', '--instance-size', help='Service container size', choices=['XS', 'S', 'M', 'L', 'XL'])
    update_parser.add_argument('-r', '--run-command', help='The command used to start the service containers')
    update_parser.add_argument('-ep', '--entrypoint', help='The entrypint used to run the command')
    update_parser.add_argument('-p', '--publish', help='Ports to publish, e.g. 5000/tcp', action='append')
    update_parser.add_argument('-ex', '--expose', help='Internal ports, e.g. 5000', action='append', type=int)
    update_parser.add_argument('-e', '--env', help='Environment variables, e.g. VAR=value', action='append')
    update_parser.add_argument('-a', '--application', help='Application service')
    update_parser.add_argument('-n', '--namespace', help='Service namespace')

    inspect_parser = service_subparsers.add_parser('inspect', help='Get details of a service', description='Get details of a service')
    inspect_parser.add_argument('name', help='Name of the service to retrieve')
    inspect_parser.add_argument('-n', '--namespace', help='Service namespace')
    inspect_parser.add_argument('-a', '--application', help='Application service')

    start_parser = service_subparsers.add_parser('start', help='Start a service', description='Start a service')
    start_parser.add_argument('name', help='Name of the service to start')
    start_parser.add_argument('-n', '--namespace', help='Service namespace')
    start_parser.add_argument('-a', '--application', help='Application service')

    stop_parser = service_subparsers.add_parser('stop', help='Stop a service', description='Stop a service')
    stop_parser.add_argument('name', help='Name of the service to stop')
    stop_parser.add_argument('-n', '--namespace', help='Service namespace')
    stop_parser.add_argument('-a', '--application', help='Application service')

    rm_parser = service_subparsers.add_parser('rm', help='Remove a service', description='Remove a service')
    rm_parser.add_argument('name', help='Name of the service to remove')
    rm_parser.add_argument('-n', '--namespace', help='Service namespace')
    rm_parser.add_argument('-a', '--application', help='Application service')

    ps_parser = service_subparsers.add_parser('ps', help='List services', description='List services')
    ps_parser.add_argument('-n', '--namespace', help='Service namespace')
    ps_parser.add_argument('-p', '--page', help='Page number', default=1)
    ps_parser.add_argument('-a', '--application', help='Application service')

    scale_parser = service_subparsers.add_parser('scale', help='Scale a service', description='Scale a service')
    scale_parser.add_argument('descriptor', nargs='*', help='E.g. web=2')
    scale_parser.add_argument('-n', '--namespace', help='Service namespace')
    scale_parser.add_argument('-a', '--application', help='Application service')

    enable_autoscaling_parser = service_subparsers.add_parser('enable-autoscaling', help='Enable auto-scaling', description='Enable auto-scaling')
    enable_autoscaling_parser.add_argument('name', help='Service name')
    enable_autoscaling_parser.add_argument('-n', '--namespace', help='Service namespace')
    enable_autoscaling_parser.add_argument('-f', '--autoscaling-config', help='Auto-scaling config file name', default='./auto-scaling.cfg')
    enable_autoscaling_parser.add_argument('-a', '--application', help='Application service')

    disable_autoscaling_parser = service_subparsers.add_parser('disable-autoscaling', help='Disable auto-scaling', description='Disable auto-scaling')
    disable_autoscaling_parser.add_argument('name', help='Service name')
    disable_autoscaling_parser.add_argument('-n', '--namespace', help='Service namespace')
    disable_autoscaling_parser.add_argument('-t', '--target-num-instances', help='Target number of instances for the service', type=int)
    disable_autoscaling_parser.add_argument('-a', '--application', help='Application service')

    logs_parser = service_subparsers.add_parser('logs', help='Query service log', description='Query service log')
    logs_parser.add_argument('name', help='Service name')
    logs_parser.add_argument('-n', '--namespace', help='Service namespace')
    logs_parser.add_argument('-s', '--start-time', help='Logs query start time. e.g. 2015-05-01 12:12:12')
    logs_parser.add_argument('-e', '--end-time', help='Logs query end time. e.g. 2015-05-01 12:12:12')
    logs_parser.add_argument('-a', '--application', help='Application service')
    logs_parser.add_argument('-t', '--tail', help='Show log in tail -f way', action='store_true')

    logs_download_parser = service_subparsers.add_parser('logs-download', help='Download service log', description='Download service log')
    logs_download_parser.add_argument('name', help='Service name')
    logs_download_parser.add_argument('-n', '--namespace', help='Service namespace')
    logs_download_parser.add_argument('-l', '--list', help='List file date', action='store_true')
    logs_download_parser.add_argument('-s', '--start-date', help='start date. e.g. 20160101')
    logs_download_parser.add_argument('-e', '--end_date', help='end date. e.g. 20160202')
    logs_download_parser.add_argument('-p', '--path', help='file saved path. e.g. /home/ubuntu/log', default='./')

    ports_parser = service_subparsers.add_parser('ports', help='Query service posts', description='Query service ports')
    ports_parser.add_argument('name', help='Service name')
    ports_parser.add_argument('-n', '--namespace', help='Service namespace')
    ports_parser.add_argument('-a', '--application', help='Application service')

    list_instance_parser = service_subparsers.add_parser('instances', help='List instances', description='List instances')
    list_instance_parser.add_argument('name', help='Service name')
    list_instance_parser.add_argument('-n', '--namespace', help='Service namespace')
    list_instance_parser.add_argument('-a', '--application', help='Application service')

    inspect_instance_parser = service_subparsers.add_parser('instance', help='Get details of an instance', description='Get details of an instance')
    inspect_instance_parser.add_argument('name', help='Service name')
    inspect_instance_parser.add_argument('id', help='Instance uuid')
    inspect_instance_parser.add_argument('-n', '--namespace', help='Service namespace')
    inspect_instance_parser.add_argument('-a', '--application', help='Application service')

    logs_instance_parser = service_subparsers.add_parser('instance-logs', help='Query instance log', description='Query instance log')
    logs_instance_parser.add_argument('name', help='Service name')
    logs_instance_parser.add_argument('id', help='Instance uuid')
    logs_instance_parser.add_argument('-s', '--start-time', help='Logs query start time. e.g. 2015-05-01 12:12:12')
    logs_instance_parser.add_argument('-e', '--end-time', help='Logs query end time. e.g. 2015-05-01 12:12:12')
    logs_instance_parser.add_argument('-n', '--namespace', help='Service namespace')
    logs_instance_parser.add_argument('-a', '--application', help='Application service')

    exec_parser = service_subparsers.add_parser('exec', help='Execute command in container', description='Execute command in container')
    exec_parser.add_argument(
        'container',
        help='Container instance name, in the form of <service name>.<container number>, where <container number> defaults to 0 if absent')
    exec_parser.add_argument('command', help='Command to execute')
    exec_parser.add_argument('args', help='Args of command', nargs=argparse.REMAINDER)
    exec_parser.add_argument('-n', '--namespace', help='Service namespace')


def _add_backups_parser(subparsers):
    backups_parser = subparsers.add_parser('backup', help='Backup operations', description='Backup operations')
    backup_subparsers = backups_parser.add_subparsers(title='Alauda backup commands', dest='subcmd')

    create_parser = backup_subparsers.add_parser('create', help='Create a new volume backup', description='Create a new volume backup')
    create_parser.add_argument('name', help='Backup name')
    create_parser.add_argument('service', help='Name of the service to create volume backup for')
    create_parser.add_argument('dir', help='Mounted volume directory to backup')
    create_parser.add_argument('-n', '--namespace', help='Service namespace')

    list_parser = backup_subparsers.add_parser('list', help='List volume backups', description='list volume backups')
    list_parser.add_argument('-n', '--namespace', help='Service namespace')

    inspect_parser = backup_subparsers.add_parser('inspect', help='Get details of a volume backup', description='Get details of a volume backup')
    inspect_parser.add_argument('id', help='UUID of the volume backup')
    inspect_parser.add_argument('-n', '--namespace', help='Service namespace')

    rm_parser = backup_subparsers.add_parser('rm', help='Remove a volume backup', description='Remove a volume backup')
    rm_parser.add_argument('id', help='UUID of the volume backup')
    rm_parser.add_argument('-n', '--namespace', help='Service namespace')


def _add_compose_parser(subparsers):
    compose_parser = subparsers.add_parser('compose', help='Compose multi-container app', description='Compose multi-container app')
    compose_subparsers = compose_parser.add_subparsers(title='Alauda compose commands', dest='subcmd')

    up_parser = compose_subparsers.add_parser('up', help='Create and start all service containers', description='Create and start all service containers')
    up_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')
    up_parser.add_argument('-s', '--strict', help='Wait for linked services to start', action='store_true')
    up_parser.add_argument('-n', '--namespace', help='Service namespace')
    up_parser.add_argument('-re', '--region', help='Region name')
    up_parser.add_argument('-i', '--ignore', help='Ignore exist services', action='store_true')

    ps_parser = compose_subparsers.add_parser('ps', help='List containers', description='Lists container')
    ps_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')
    ps_parser.add_argument('-n', '--namespace', help='Service namespace')

    start_parser = compose_subparsers.add_parser('start', help='Start all service containers', description='Start all service containers')
    start_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')
    start_parser.add_argument('-s', '--strict', help='Wait for linked services to start', action='store_true')
    start_parser.add_argument('-n', '--namespace', help='Service namespace')

    stop_parser = compose_subparsers.add_parser('stop', help='Stop all service containers', description='Stop all service containers')
    stop_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')
    stop_parser.add_argument('-n', '--namespace', help='Service namespace')

    restart_parser = compose_subparsers.add_parser('restart', help='Restart all service containers', description='Restart all service containers')
    restart_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')
    restart_parser.add_argument('-s', '--strict', help='Wait for linked services to start', action='store_true')
    restart_parser.add_argument('-n', '--namespace', help='Service namespace')

    rm_parser = compose_subparsers.add_parser('rm', help='Remove all service containers', description='Remove all service containers')
    rm_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')
    rm_parser.add_argument('-n', '--namespace', help='Service namespace')

    scale_parser = compose_subparsers.add_parser(
        'scale',
        help='Set number of containers to run for a service',
        description='Set number of containers to run for a service')
    scale_parser.add_argument('descriptor', nargs='*', help='E.g. web=2 db=1')
    scale_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')
    scale_parser.add_argument('-n', '--namespace', help='Service namespace')


def _add_organization_parser(subparsers):
    org_parser = subparsers.add_parser('organization', help='Organization operations', description='Organization operations')
    org_subparsers = org_parser.add_subparsers(title='Alauda organization commands', dest='subcmd')

    org_subparsers.add_parser('list', help='List all organization', description='List all organization')

    create_parser = org_subparsers.add_parser('create', help='Create a new organization', description='Create a new organization')
    create_parser.add_argument('name', help='Organization name')
    create_parser.add_argument('company', help='Company name')

    inspect_parser = org_subparsers.add_parser('inspect', help='Get details of an organization', description='Get details of an organization')
    inspect_parser.add_argument('name', help='Organization name')

    update_parser = org_subparsers.add_parser('update', help='Update an exist orgnization', description='Update an exist orgnization')
    update_parser.add_argument('name', help='Organization name')
    update_parser.add_argument('company', help='Company name')


def _add_build_parser(subparsers):
    build_parser = subparsers.add_parser('build', help='Build operations', description='Build operations')
    build_subparsers = build_parser.add_subparsers(title='Alauda build commands', dest='subcmd')

    create_parser = build_subparsers.add_parser(
        'create', help='Create a build', description='Create a build'
    )
    create_parser.add_argument('-p', '--path', help='Source code path', dest='source')
    create_parser.add_argument('-rn', '--repo-name', help='Repository name', dest='repo_name')
    create_parser.add_argument('-n', '--namespace', help='Repository namespace', dest='namespace')
    create_parser.add_argument('-t', '--tag', help='Image tag', dest='image_tag')
    create_parser.add_argument('-i', '--commit-id', help='Commit id', dest='commit_id')


def _add_application_parser(subparsers):
    app_parser = subparsers.add_parser('app', help='Application operations', description='Application operations')
    app_subparsers = app_parser.add_subparsers(title='Alauda application commands', dest='subcmd')

    create_parser = app_subparsers.add_parser('create', help='Create an application', description='Create an application')
    create_parser.add_argument('name', help='Application name')
    create_parser.add_argument('-n', '--namespace', help='Application namespace')
    create_parser.add_argument('-re', '--region', help='Region name', default='BEIJING1')
    create_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')

    run_parser = app_subparsers.add_parser('run', help='Run an application', description='Run an application')
    run_parser.add_argument('name', help='Application name')
    run_parser.add_argument('-n', '--namespace', help='Application namespace')
    run_parser.add_argument('-re', '--region', help='Region name', default='BEIJING1')
    run_parser.add_argument('-f', '--file', help='Compose file name', default='./docker-compose.yml')

    inspect_parser = app_subparsers.add_parser('inspect', help='Inspect an application', description='Inspect an application')
    inspect_parser.add_argument('name', help='Application name')
    inspect_parser.add_argument('-n', '--namespace', help='Application namespace')

    start_parser = app_subparsers.add_parser('start', help='Start an application', description='Start an application')
    start_parser.add_argument('name', help='Application name')
    start_parser.add_argument('-n', '--namespace', help='Application namespace')

    stop_parser = app_subparsers.add_parser('stop', help='Stop an application', description='Stop an application')
    stop_parser.add_argument('name', help='Application name')
    stop_parser.add_argument('-n', '--namespace', help='Application namespace')

    rm_parser = app_subparsers.add_parser('rm', help='Remove an application', description='Remove an application')
    rm_parser.add_argument('name', help='Application name')
    rm_parser.add_argument('-n', '--namespace', help='Application namespace')
