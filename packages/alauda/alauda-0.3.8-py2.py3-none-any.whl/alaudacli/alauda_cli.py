import sys
import copy
import traceback

import cmd_parser
import cmd_processor
from exceptions import AlaudaInputError


def patch_argv(argv):
    args = copy.copy(argv)

    if not args:
        raise AlaudaInputError('Arguments cannot be empty')

    if len(args) >= 2:
        if args[1] in ['create', 'run', 'scale', 'inspect', 'start', 'stop', 'rm',
                       'enable-autoscaling', 'disable-autoscaling', 'logs', 'ps',
                       'instances', 'instance', 'instance-logs', 'exec', 'update']:
            args.insert(1, 'service')

    if len(args) == 1:
        args.append('-h')
    elif len(args) == 2 and args[1] in ['service', 'compose', 'backup', 'organization', 'build', 'app']:
        args.append('-h')
    elif len(args) == 3:
        if args[1] == 'service' and args[2] in ['create', 'run', 'scale', 'inspect', 'start', 'stop', 'rm',
                                                'enable-autoscaling', 'disable-autoscaling', 'logs',
                                                'instances', 'instance', 'instance-logs', 'exec', 'ports', 'update']:
            args.append('-h')
        elif args[1] == 'compose' and args[2] in ['scale']:
            args.append('-h')
        elif args[1] == 'backup' and args[2] in ['create', 'inspect', 'rm']:
            args.append('-h')
        elif args[1] == 'organization' and args[2] in ['create', 'inspect', 'update']:
            args.append('-h')
        elif args[1] == 'build' and args[2] in ['create']:
            args.append('-h')
        elif args[1] == 'app' and args[2] in ['create']:
            args.append('-h')

    return args[1:]


def main():
    try:
        argv = patch_argv(sys.argv)
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
    except Exception as ex:
        print ex
        traceback.print_exc()
        sys.exit(1)
    print '[alauda] OK'

if __name__ == '__main__':
    main()
