import unittest
import mock
import json
from alaudacli import cmd_parser, cmd_processor, util, auth


class UtilTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_parse_image_name_tag(self):
        name, tag = util.parse_image_name_tag('index/user/repo:tag')
        self.assertEqual('index/user/repo', name)
        self.assertEqual('tag', tag)

    def test_parse_image_name_no_tag(self):
        name, tag = util.parse_image_name_tag('index/user/repo')
        self.assertEqual('index/user/repo', name)
        self.assertEqual('latest', tag)

    def test_parse_target_state(self):
        state = util.parse_target_state(True)
        self.assertEqual('STARTED', state)
        state = util.parse_target_state(False)
        self.assertEqual('STOPPED', state)

    def test_parse_instance_ports(self):
        ports, _ = util.parse_instance_ports(['80/tcp', '22'])
        self.assertEqual([{'endpoint_type': 'tcp-endpoint', 'container_port': 80, 'protocol': 'tcp'},
                          {'endpoint_type': 'tcp-endpoint', 'container_port': 22, 'protocol': 'tcp'}], ports)

    def test_parse_envvars(self):
        envvars = util.parse_envvars(['FOO=foo', 'BAR:bar', {'BAZ': 'baz'}, 'A=', 'A= '])
        self.assertEqual({'FOO': 'foo', 'BAR': 'bar', 'BAZ': 'baz', 'A': '', 'A': ' '}, envvars)

    def test_parse_volumes(self):
        volumes = util.parse_volumes(['/var/lib/data1:10', '/var/lib/data2:20'])
        self.assertEqual([{'app_volume_dir': '/var/lib/data1', 'volume_type': 'EBS', 'size_gb': 10},
                          {'app_volume_dir': '/var/lib/data2', 'volume_type': 'EBS', 'size_gb': 20}], volumes)

    def test_build_headers(self):
        headers = auth.build_headers('toooooken')
        self.assertEqual({'Authorization': 'Token toooooken', 'Content-type': 'application/json'}, headers)

    def test_parse_links(self):
        links = util.parse_links(['mysql:db', 'redis:db1'])
        self.assertEqual([('mysql', 'db'), ('redis', 'db1')], links)

    def test_parse_scale(self):
        scale_dict = util.parse_scale(['mysql=3', 'redis=2'])
        self.assertEqual({'mysql': 3, 'redis': 2}, scale_dict)

    def test_parse_autoscale_info(self):
        mode, cfg = util.parse_autoscale_info((True, './example/auto-scaling.cfg'))
        self.assertEqual('AUTO', mode)
        result = {
            "metric_name": "CPU_UTILIZATION",
            "metric_stat": "MEAN",
            "upper_threshold": 0.94999999999999996,
            "lower_threshold": 0.5,
            "decrease_delta": 1,
            "increase_delta": 1,
            "minimum_num_instances": 2,
            "maximum_num_instances": 5,
            "wait_period": 120
        }
        self.assertEqual(json.loads(cfg), result)

    def test_expand_environment(self):
        envvars = {
            'FOO': 'foo',
            'BAR': 'bar',
            'BAZ': '$FOO:$BAR',
            'FOOBAR': '$FOO-$FOO-$BAR-$BAR-$BOO'
        }
        util.expand_environment(envvars)
        self.assertEqual('foo', envvars['FOO'])
        self.assertEqual('bar', envvars['BAR'])
        self.assertEqual('foo:bar', envvars['BAZ'])
        self.assertEqual('foo-foo-bar-bar-$BOO', envvars['FOOBAR'])


class ProcessCmdTest(unittest.TestCase):

    def setUp(self):
        pass

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_login(self, mock_commands):
        argv = ['login', '-u', 'user', '-p', 'password', '-c', 'io']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.login.assert_called_with('user', 'password', 'io', None)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_logout(self, mock_commands):
        argv = ['logout']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.logout.assert_called()

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_create(self, mock_commands):
        argv = ['service', 'create', 'hello', 'index.alauda.io/alauda/hello-world:latest',
                '-t', '2', '-s', 'XS', '-r', '/run.sh', '-ep', '/bin/bash',
                '-e', 'FOO=bar', '-p', '5000/tcp', '-v', '/var/lib/data1:10', '-l', 'myql:db',
                '-a', '-f', './auto-scaling.cfg', '-n', 'myns', '-d', 'my.com', '-re', 'myregion']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_create.assert_called_with(image='index.alauda.io/alauda/hello-world:latest',
                                                        name='hello', start=False, target_num_instances=2, instance_size='XS',
                                                        run_command='/run.sh', entrypoint='/bin/bash', env=['FOO=bar'], ports=['5000/tcp'], exposes=None,
                                                        volumes=['/var/lib/data1:10'], links=['myql:db'], scaling_info=(True, './auto-scaling.cfg'),
                                                        namespace='myns', custom_domain_name='my.com', region_name='myregion')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_run(self, mock_commands):
        argv = ['service', 'run', 'hello', 'index.alauda.io/alauda/hello-world:latest',
                '-t', '2', '-s', 'XS', '-r', '/run.sh', '-ep', '/bin/bash',
                '-e', 'FOO=bar', '-p', '5000/tcp', '-v', '/var/lib/data1:10', '-l', 'db',
                '-f', './auto-scaling.cfg', '-n', 'myns', '-d', 'my.com', '-re', 'myregion']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_create.assert_called_with(image='index.alauda.io/alauda/hello-world:latest',
                                                        name='hello', start=True, target_num_instances=2, instance_size='XS',
                                                        run_command='/run.sh', entrypoint='/bin/bash', env=['FOO=bar'], ports=['5000/tcp'], exposes=None,
                                                        volumes=['/var/lib/data1:10'], links=['db'], scaling_info=(False, './auto-scaling.cfg'),
                                                        namespace='myns', custom_domain_name='my.com', region_name='myregion')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_scale(self, mock_commands):
        argv = ['service', 'scale', 'mysql=2 redis=3']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_scale.assert_called_with(['mysql=2 redis=3'], None, app=None)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_enable_autoscaling(self, mock_commands):
        argv = ['service', 'enable-autoscaling', 'hello', '-f', 'auto-scaling.cfg']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_enable_autoscaling.assert_called_with('hello', None, 'auto-scaling.cfg', app=None)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_disable_autoscaling(self, mock_commands):
        argv = ['service', 'disable-autoscaling', 'hello', '-t', '2']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_disable_autoscaling.assert_called_with('hello', None, 2, app=None)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_inspect(self, mock_commands):
        argv = ['service', 'inspect', 'hello']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_inspect.assert_called_with('hello', namespace=None, app=None)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_start(self, mock_commands):
        argv = ['service', 'start', 'hello']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_start.assert_called_with('hello', namespace=None, app=None)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_stop(self, mock_commands):
        argv = ['service', 'stop', 'hello']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_stop.assert_called_with('hello', namespace=None, app=None)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_rm(self, mock_commands):
        argv = ['service', 'rm', 'hello']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_rm.assert_called_with('hello', namespace=None, app=None)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_exec(self, mock_commands):
        argv = ['service', 'exec', 'hello', '/bin/ls', '-l']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_exec.assert_called_with('hello', None, '/bin/ls', '-l')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_service_ps(self, mock_commands):
        argv = ['service', 'ps']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.service_ps.assert_called_with(namespace=None, page=1, app=None)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_compose_up(self, mock_commands):
        argv = ['compose', 'up', '-s', '-n', 'myns', '-re', 'myregion']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.compose_up.assert_called_with('./docker-compose.yml', True, 'myns', 'myregion', False)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_compose_ps(self, mock_commands):
        argv = ['compose', 'ps', '-n', 'myns']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.compose_ps.assert_called_with('./docker-compose.yml', 'myns')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_compose_start(self, mock_commands):
        argv = ['compose', 'start', '-n', 'myns']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.compose_start.assert_called_with('./docker-compose.yml', False, 'myns')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_compose_stop(self, mock_commands):
        argv = ['compose', 'stop', '-n', 'myns']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.compose_stop.assert_called_with('./docker-compose.yml', 'myns')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_compose_restart(self, mock_commands):
        argv = ['compose', 'restart', '-n', 'myns']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.compose_restart.assert_called_with('./docker-compose.yml', False, 'myns')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_compose_rm(self, mock_commands):
        argv = ['compose', 'rm', '-n', 'myns']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.compose_rm.assert_called_with('./docker-compose.yml', 'myns')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_compose_scale(self, mock_commands):
        argv = ['compose', 'scale', 'redis=2 web=3', '-n', 'myns']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.compose_scale.assert_called_with(['redis=2 web=3'], './docker-compose.yml', 'myns')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_backup_create(self, mock_commands):
        argv = ['backup', 'create', 'my_snapshot', 'hello', '/data']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.backup_create.assert_called_with('my_snapshot', 'hello', '/data', None)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_backup_list(self, mock_commands):
        argv = ['backup', 'list']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.backup_list.assert_called_with(None)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_backup_inspect(self, mock_commands):
        argv = ['backup', 'inspect', 'my_backup_id']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.backup_inspect.assert_called_with('my_backup_id', None)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_backup_rm(self, mock_commands):
        argv = ['backup', 'rm', 'my_backup_id']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.backup_rm.assert_called_with('my_backup_id', None)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_instance_ps(self, mock_commands):
        argv = ['service', 'instances', 'hello']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.instance_ps.assert_called_with('hello', namespace=None, app=None)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_instance_inspect(self, mock_commands):
        argv = ['service', 'instance', 'hello', 'd938a2d7-0071-11e5-ab5d-02416b28d26a']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.instance_inspect.assert_called_with('hello', 'd938a2d7-0071-11e5-ab5d-02416b28d26a', namespace=None, app=None)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_instance_logs(self, mock_commands):
        argv = ['service', 'instance-logs', 'hello', 'd938a2d7-0071-11e5-ab5d-02416b28d26a']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.instance_logs.assert_called_with('hello', 'd938a2d7-0071-11e5-ab5d-02416b28d26a', None, None, None, app=None)

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_organization_create(self, mock_commands):
        argv = ['organization', 'create', 'myorgs', 'mathilde']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.organization_create.assert_called_with('myorgs', 'mathilde')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_organization_inspect(self, mock_commands):
        argv = ['organization', 'inspect', 'myorgs']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.organization_inspect.assert_called_with('myorgs')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_organization_update(self, mock_commands):
        argv = ['organization', 'update', 'myorgs', 'alauda']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.organization_update.assert_called_with('myorgs', 'alauda')

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_organization_list(self, mock_commands):
        argv = ['organization', 'list']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.organization_list.assert_called_with()

    @mock.patch('alaudacli.cmd_processor.commands')
    def test_process_build_create(self, mock_commands):
        argv = ['build', 'create', '-p', '/tmp/alaudacli/test', '-rn', 'fileupload-test',
                '-n', 'alauda', '-t', 'latest', '-i', 'abcdefg']
        args = cmd_parser.parse_cmds(argv)
        cmd_processor.process_cmds(args)
        mock_commands.build_create.assert_called_with('fileupload-test',
                                                      '/tmp/alaudacli/test',
                                                      'alauda', 'latest',
                                                      'abcdefg')
