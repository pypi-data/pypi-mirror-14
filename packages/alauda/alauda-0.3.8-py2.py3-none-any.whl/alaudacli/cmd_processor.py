from . import commands


def process_cmds(args):
    if args.cmd == 'login':
        commands.login(args.username, args.password, args.cloud, args.endpoint)
    elif args.cmd == 'logout':
        commands.logout()
    elif args.cmd == 'service':
        if args.subcmd == 'create':
            commands.service_create(image=args.image, name=args.name, start=False, target_num_instances=args.target_num_instances,
                                    instance_size=args.instance_size, run_command=args.run_command, entrypoint=args.entrypoint, env=args.env,
                                    ports=args.publish, exposes=args.expose, volumes=args.volume, links=args.link, namespace=args.namespace,
                                    scaling_info=(args.autoscale, args.autoscaling_config), custom_domain_name=args.domain, region_name=args.region)
        elif args.subcmd == 'run':
            commands.service_create(image=args.image, name=args.name, start=True, target_num_instances=args.target_num_instances,
                                    instance_size=args.instance_size, run_command=args.run_command, entrypoint=args.entrypoint, env=args.env,
                                    ports=args.publish, exposes=args.expose, volumes=args.volume, links=args.link, namespace=args.namespace,
                                    scaling_info=(args.autoscale, args.autoscaling_config), custom_domain_name=args.domain, region_name=args.region)
        elif args.subcmd == 'update':
            commands.service_update(name=args.name, image_tag=args.tag, target_num_instances=args.target_num_instances, instance_size=args.instance_size,
                                    run_command=args.run_command, entrypoint=args.entrypoint, env=args.env, ports=args.publish, exposes=args.expose,
                                    namespace=args.namespace, app=args.application)
        elif args.subcmd == 'inspect':
            commands.service_inspect(args.name, namespace=args.namespace, app=args.application)
        elif args.subcmd == 'start':
            commands.service_start(args.name, namespace=args.namespace, app=args.application)
        elif args.subcmd == 'stop':
            commands.service_stop(args.name, namespace=args.namespace, app=args.application)
        elif args.subcmd == 'rm':
            commands.service_rm(args.name, namespace=args.namespace, app=args.application)
        elif args.subcmd == 'ps':
            commands.service_ps(namespace=args.namespace, page=args.page, app=args.application)
        elif args.subcmd == 'scale':
            commands.service_scale(args.descriptor, args.namespace, app=args.application)
        elif args.subcmd == 'enable-autoscaling':
            commands.service_enable_autoscaling(args.name, args.namespace, args.autoscaling_config, app=args.application)
        elif args.subcmd == 'disable-autoscaling':
            commands.service_disable_autoscaling(args.name, args.namespace, args.target_num_instances, app=args.application)
        elif args.subcmd == 'logs':
            commands.service_logs(args.name, args.namespace, args.start_time, args.end_time, app=args.application, tail=args.tail)
        elif args.subcmd == 'logs-download':
            commands.service_logs_download(args.name, args.namespace, args.list, args.start_date, args.end_date, args.path)
        elif args.subcmd == 'ports':
            commands.service_ports(args.name, args.namespace, app=args.application)
        elif args.subcmd == 'instances':
            commands.instance_ps(args.name, namespace=args.namespace, app=args.application)
        elif args.subcmd == 'instance':
            commands.instance_inspect(args.name, args.id, namespace=args.namespace, app=args.application)
        elif args.subcmd == 'instance-logs':
            commands.instance_logs(args.name, args.id, args.namespace, args.start_time, args.end_time, app=args.application)
        elif args.subcmd == 'exec':
            commands.service_exec(args.container, args.namespace, args.command, *args.args)
    elif args.cmd == 'backup':
        if args.subcmd == 'create':
            commands.backup_create(args.name, args.service, args.dir, args.namespace)
        elif args.subcmd == 'list':
            commands.backup_list(args.namespace)
        elif args.subcmd == 'inspect':
            commands.backup_inspect(args.id, args.namespace)
        elif args.subcmd == 'rm':
            commands.backup_rm(args.id, args.namespace)
    elif args.cmd == 'compose':
        if args.subcmd == 'up':
            commands.compose_up(args.file, args.strict, args.namespace, args.region, args.ignore)
        elif args.subcmd == 'ps':
            commands.compose_ps(args.file, args.namespace)
        elif args.subcmd == 'start':
            commands.compose_start(args.file, args.strict, args.namespace)
        elif args.subcmd == 'stop':
            commands.compose_stop(args.file, args.namespace)
        elif args.subcmd == 'restart':
            commands.compose_restart(args.file, args.strict, args.namespace)
        elif args.subcmd == 'rm':
            commands.compose_rm(args.file, args.namespace)
        elif args.subcmd == 'scale':
            commands.compose_scale(args.descriptor, args.file, args.namespace)
    elif args.cmd == 'organization':
        if args.subcmd == 'create':
            commands.organization_create(args.name, args.company)
        elif args.subcmd == 'list':
            commands.organization_list()
        elif args.subcmd == 'inspect':
            commands.organization_inspect(args.name)
        elif args.subcmd == 'update':
            commands.organization_update(args.name, args.company)
    elif args.cmd == 'build':
        if args.subcmd == 'create':
            commands.build_create(
                args.repo_name, args.source, args.namespace, args.image_tag,
                args.commit_id
            )
    elif args.cmd == 'app':
        if args.subcmd == 'create':
            commands.app_create(args.name, args.namespace, args.region, args.file)
        if args.subcmd == 'run':
            commands.app_run(args.name, args.namespace, args.region, args.file)
        elif args.subcmd == 'inspect':
            commands.app_inspect(args.name, args.namespace)
        elif args.subcmd == 'start':
            commands.app_start(args.name, args.namespace)
        elif args.subcmd == 'stop':
            commands.app_stop(args.name, args.namespace)
        elif args.subcmd == 'rm':
            commands.app_rm(args.name, args.namespace)
