import json
import requests
import os
import auth
import util
import yaml
from compose import resolve_extends
from exceptions import AlaudaInputError


class Application(object):

    def __init__(self, name, region=None, file=None, namespace=None):
        self.api_endpoint, self.token, self.username = auth.load_token()
        self.name = name
        self.file = file
        self.namespace = namespace or self.username
        self.region = region
        self.headers = auth.build_headers(self.token)
#         self.headers['Content-type'] = 'multipart/form-data; boundary=simple boundary'
        del self.headers['Content-type']

    def create(self):
        try:
            app_info = self.load_app_file(self.file)
            self.remove_extend_keyword(app_info)
            files = {'services': ('{}.yml'.format(self.name), json.dumps(app_info))}
        except:
            files = ''
        url = '{}applications/{}/'.format(self.api_endpoint, self.namespace)
        data = {'app_name': self.name, 'region': self.region, 'namespace': self.namespace}
        print self.headers
        r = requests.request("POST", url, headers=self.headers, data=data, files=files)
        util.check_response(r)

    def get(self):
        url = '{}applications/{}/{}/'.format(self.api_endpoint, self.namespace, self.name)
        r = requests.get(url=url, headers=self.headers)
        util.check_response(r)
        services = json.loads(r.text)
        services = services['services']
        return services

    def start(self):
        url = '{}applications/{}/{}/start/'.format(self.api_endpoint, self.namespace, self.name)
        r = requests.put(url=url, headers=self.headers)
        util.check_response(r)

    def stop(self):
        url = '{}applications/{}/{}/stop/'.format(self.api_endpoint, self.namespace, self.name)
        r = requests.put(url=url, headers=self.headers)
        util.check_response(r)

    def remove(self):
        url = '{}applications/{}/{}/'.format(self.api_endpoint, self.namespace, self.name)
        r = requests.delete(url=url, headers=self.headers)
        util.check_response(r)

    def load_app_file(self, filepath):
        abspath = os.path.abspath(filepath)
        compose_data = self.load_yaml(abspath)
        vertex_list = [abspath]
        edge_list = []
        resolve_extends(compose_data, abspath, vertex_list, edge_list)
        return compose_data

    def load_yaml(self, filepath):
        try:
            with open(filepath, 'r') as f:
                return yaml.safe_load(f)
        except:
            raise AlaudaInputError('Missing or invalid compose yaml file at {}.'.format(filepath))

    def remove_extend_keyword(self, app_info):
        for k in app_info.keys():
            if 'extends' in app_info[k].keys():
                del app_info[k]['extends']
