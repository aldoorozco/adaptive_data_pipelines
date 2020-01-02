from storage import Storage
from clients import Clients
from metadata import Metadata
from datetime import datetime
from os.path import dirname, isfile

import requests
import json
import time
import os

class Job:
    storage = Storage()
    fs_mountpoint = '/app/root'
    datapoints_per_partition = 140000
    minimum_partitions = 6
    def __init__(self):
       pass 

    @staticmethod
    def run(configs):
        foundation_output = Job.get_infrastructure_output('foundation')
        superserver_output = Job.get_infrastructure_output('superserver')

        sources_count = int(configs['source_count'])

        for i in range(1, sources_count + 1):
            local_source_path = Job.fs_mountpoint + configs[f'source{i}_path']
            metadata = Job.get_metadata(local_source_path).__dict__
            remote_path = Job.migrate(foundation_output['datalake_bucket'], local_source_path, i)

            configs['partitions'] = int(int(metadata['columns_count'] * metadata['rows_count'])\
                                    / Job.datapoints_per_partition)\
                                    + Job.minimum_partitions\
                                    + configs.get('partitions', 0)
            configs[f'source{i}_path'] = remote_path

        configs['public_subnet_id'] = foundation_output['public_subnet_id']
        configs['private_subnet_id'] = foundation_output['private_subnet_id']
        configs['superserver_security_group'] = foundation_output['superserver_security_group']
        configs['master_security_group'] = foundation_output['master_security_group']
        configs['slave_security_group'] = foundation_output['slave_security_group']
        configs['crawler_role_arn'] = foundation_output['glue_role']
        configs['logs_path'] = 's3://' + foundation_output['logs_bucket']
        configs['destination_path'] = 's3://' + foundation_output['datamart_bucket']
        configs['service_access_sg'] = foundation_output['emr_role']

        Job.create_dag(superserver_output['public_ip'], configs)

    @staticmethod
    def get_metadata(file_path=None, database=None, table=None):
        metadata = None
        if file_path and isfile(file_path):
            if file_path.endswith('csv'):
                metadata = Metadata('csv', filename=file_path) 
            elif file_path.endswith('xlsx'):
                metadata = Metadata('xlsx', filename=file_path)
            elif file_path.endswith('json'):
                metadata = Metadata('json', filename=file_path)
            else:
                raise Exception(f'[Error] Unsupported file extension {file_path}')
        elif database is not None and table is not None:
            metadata = Metadata('mysql', database=database, table=table)
        else:
            raise Exception(f'[Error] Invalid database/table {database}/{table}')
        return metadata

    @staticmethod
    def migrate(datalake_bucket, source_path, source_id):
        str_date = datetime.now().strftime('%Y%m%d')

        return Job.storage.multi_part_copy(source_path, datalake_bucket, f'{str_date}/{source_id}')

    @staticmethod
    def create_dag(superserver_ip, configs):
        output = Job.send_request(superserver_ip, '5000', 'create_dag', 'post', configs)
        print(f'Got response {output}')

    @staticmethod
    def send_request(service, port, path, method, data=None):
        url = f'http://{service}:{port}/{path}'
        resp = None
        if method == 'post':
            resp = requests.post(url, json=data)
        elif method == 'get':
            resp = requests.get(url)
        else:
            print(f'Unsupported method {method}')
        return resp

    @staticmethod
    def get_infrastructure_output(module):
        resp = Job.send_request('infrastructure', '5000', f'outputs/modules/{module}', 'get')

        if resp.status_code != 200:
            print(f'Request: status code {resp.status_code}, json {resp.json()}')
        return resp.json()['output']
