from service import Service
import util
import copy
import time
from exceptions import AlaudaServerError

MAX_CREATE_TIME = 300
MAX_ERROR_TIME = 30


class Project(object):

    def __init__(self, services):
        self.services = services

    def up(self, ignore):
        for service_level in self.services:
            for service in service_level:
                try:
                    service.run()
                except AlaudaServerError as ex:
                    if str(ex).find('App {} already exists'.format(service.name)) > -1 and ignore:
                        print 'Ignore exist service -> {}'.format(service.name)
                        continue
                    else:
                        raise ex

    def strict_up(self, ignore):
        started_list = []
        for i in range(len(self.services) - 1):
            for service in self.services[i]:
                try:
                    service.run()
                except AlaudaServerError as ex:
                    if str(ex).find('App {} already exists'.format(service.name)) > -1 and ignore:
                        continue
                    else:
                        print 'error: {}'.format(ex.message)
                        raise ex
            started_list.extend(self.services[i])
            ret = self._wait_services_ready(self.services[i])
            if ret is not None:
                for service in started_list:
                    Service.remove(service.name)
                raise AlaudaServerError(500, ret)
        for service in self.services[len(self.services) - 1]:
            try:
                service.run()
            except AlaudaServerError as ex:
                if str(ex).find('App {} already exists'.format(service.name)) > -1 and ignore:
                    print 'Ignore exist service -> {}'.format(service.name)
                    continue
                else:
                    raise ex

    def ps(self, namespace):
        service_list = self._get_service_list(namespace)
        util.print_ps_output(service_list)

    def start(self):
        for service_level in self.services:
            for service in service_level:
                service.start()

    def strict_start(self):
        started_list = []
        for i in range(len(self.services) - 1):
            for service in self.services[i]:
                service.start()
            started_list.extend(self.services[i])
            ret = self._wait_services_ready(self.services[i])
            if ret is not None:
                for service in started_list:
                    Service.remove(service.name)
                raise AlaudaServerError(500, ret)
        for service in self.services[len(self.services) - 1]:
            service.start()

    def stop(self):
        for service_level in self.services:
            for service in service_level:
                service.stop()

    def restart(self):
        for service_level in self.services:
            for service in service_level:
                service.stop()
        for service_level in self.services:
            for service in service_level:
                service.start()

    def strict_restart(self):
        for service_level in self.services:
            for service in service_level:
                service.stop()
        started_list = []
        for i in range(len(self.services) - 1):
            for service in self.services[i]:
                service.start()
            started_list.extend(self.services[i])
            ret = self._wait_services_ready(self.services[i])
            if ret is not None:
                for service in started_list:
                    Service.remove(service.name)
                raise AlaudaServerError(ret)
        for service in self.services[len(self.services) - 1]:
            service.start()

    def rm(self, namespace):
        for service_level in self.services:
            for service in service_level:
                Service.remove(service.name, namespace)

    def scale(self, scale_dict, namespace):
        for name, number in scale_dict.items():
            service = Service.fetch(name, namespace)
            service.scale(number)

    def _get_service_list(self, namespace):
        service_list = []
        for service_level in self.services:
            for service in service_level:
                try:
                    service_list.append(Service.fetch(service.name, namespace))
                except AlaudaServerError:
                    continue
        return service_list

    def _wait_services_ready(self, service_list):
        services = copy.copy(service_list)
        start_time = int(time.time())
        while len(services) > 0:
            time.sleep(5)
            for i in range(len(services))[::-1]:
                service = Service.fetch(services[i].name)
                state = service.get_state()
                if state == 'Deploying':
                    print 'Service {} is deploying'.format(services[i].name)
                    continue
                elif state == 'Running':
                    print 'Start service {} success!'.format(services[i].name)
                    services.remove(services[i])
                    continue
                elif state == 'Stopped' and int(time.time()) - start_time < MAX_ERROR_TIME:
                    continue
                else:
                    return 'Create/Start {0} fail! State is: {1}'.format(services[i].name, state)
            current_time = int(time.time())
            if current_time - start_time > MAX_CREATE_TIME:
                return 'Time out'
        return None
