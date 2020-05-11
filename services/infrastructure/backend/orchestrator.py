from python_terraform import *
from os import listdir
from os.path import isdir, join
from copy import deepcopy
from threading import Thread

import requests
import json

class Orchestrator:
    states = [
        'INITIALIZING',
        'SETTING UP FOUNDATION',
        'SETTING UP SUPERSERVER',
        'READY'
    ]

    def __init__(self):
        terraform_path = '/app/terraform/AWS'
        default_service_metadata = {'created': False, 'outputs': None}
        supported_services = self.__get_supported_services(f'{terraform_path}/modules')
        self.__services = {svc: default_service_metadata.copy() for svc in supported_services}
        self.__tf = Terraform(working_dir=terraform_path)
        self.__default_options = {
            'auto_approve': IsFlagged,
            'target': ['module.{}'],
            'capture_output': False
        }
        thread = Thread(target=self.initialize_infra, args=())
        thread.daemon = True
        thread.start()
        self.__status_index = 0
        self.__status = Orchestrator.states[0]

    def update_status(self):
        if self.__status_index < (len(Orchestrator.states) - 1):
            self.__status_index += 1
            self.__status = Orchestrator.states[self.__status_index]

    def initialize_infra(self):
        # Initialize terraform
        self.__execute_infra_cmd(
            module=None,
            cmd='init',
            options={'capture_output': False},
            overwrite_options=True
        )
        self.update_status()
        ip = requests.get('https://api.ipify.org').text

        self.__spin_up_services(ip)

    def __spin_up_services(self, ip):
        # Start the module by setting up the foundation
        foundation_options = {'var':{'local_ip': ip}}

        self.setup_module('foundation', foundation_options)

        self.update_status()
        # Superserver requires both a public_subnet_id and a security_group
        outputs = self.__services['foundation']['outputs']
        print(outputs)
        superserver_options = {
            'var': {
                "public_subnet_id": outputs['public_subnet_id'],
                "security_group": outputs['superserver_security_group'],
                "superserver_role": outputs['superserver_role'],
                "superserver_keypair": outputs['superserver_keypair']
            }
        }
        self.setup_module(
            'superserver',
            superserver_options
        )
        self.update_status()

    def __get_supported_services(self, path):
        #return [f for f in listdir(path) if isdir(join(path, f))]
        return ['foundation', 'superserver']

    def __execute_infra_cmd(self, module, cmd, options=None, overwrite_options=False):
        if overwrite_options:
            d = options
        else:
            d = deepcopy(self.__default_options)
            d['target'][0] = d['target'][0].format(module)
            if options and type(options) is dict:
                d.update(options)

        if d:
            _, stdout, _ = self.__tf.cmd(cmd, **d)
        else:
            _, stdout, _ = self.__tf.cmd(cmd)
        return stdout

    def __assert_module(self, module):
        if not module or module not in self.__services:
            raise Exception(f'Unsupported module {module}. Only {self.__services.keys()} are supported')

    def setup_module(self, module, options=None):
        self.__assert_module(module)
        output_options = {
            'capture_output': True,
            'json': IsFlagged
        }

        if not self.__services[module]['created']:
            self.__execute_infra_cmd(
                module,
                'apply',
                options
            )
            stdout = self.__execute_infra_cmd(
                module,
                'output',
                output_options,
                True
            )
            json_out = json.loads(stdout)
            # Only filter those variables that belong to this module
            self.__services[module]['outputs'] = {
                k.replace(f'{module}_', ''): v['value'] for k, v in json_out.items() if module in k
            }
            self.__services[module]['created'] = True
        else:
            print(f'Module {module} already up and running')

    def teardown_module(self, module):
        self.__assert_module(module)

        if self.__services[module]['created']:
            self.__execute_infra_cmd(module, 'destroy')
            self.__services[module]['created'] = False
            self.__services[module]['outputs'] = None
        else:
            print(f'Module {module} already down')

    def get_output(self, module):
        self.__assert_module(module)

        if self.__status != 'READY':
            return 'Infrastructure setup ongoing', {}

        output = {'output': self.__services[module]['outputs']}

        return None, output

    def get_status(self):
        return {'status': self.__status}

    def cleanup(self):
        self.__execute_infra_cmd(
            module='superserver',
            cmd='destroy',
            options={'capture_output': False, 'auto_approve': IsFlagged},
            overwrite_options=True
        )
        self.__execute_infra_cmd(
            module='foundation',
            cmd='destroy',
            options={'capture_output': False, 'auto_approve': IsFlagged},
            overwrite_options=True
        )
