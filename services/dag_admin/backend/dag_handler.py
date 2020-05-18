from clients import Clients
from storage import Storage
from os.path import basename

import requests
import re
import json
import time
import os

class DagHandler:
    glue_client = Clients.glue_client
    storage = Storage()
    bucket = 'abdp-templates'
    key = 'spark'
    template = storage.copy_bucket(
         '/app/template/target/tog-0.1.jar',
         bucket,
         key
    )
    #table_name_regex = re.compile(r'.*from `?([\.\w]+)`?.*')

    def __init__(self):
        pass

    @staticmethod
    def run(configs):
        configs['sql_query'] = configs['sql_query'].lower().replace('\n', ' ')

        source_count = int(configs['source_count'])

        crawler_role_arn = configs['crawler_role_arn']

        for i in range(1, source_count + 1):
            print(f'source{i}_path')
            print(f'source{i}_table')
            source_path = configs[f'source{i}_path']
            source_table = configs[f'source{i}_table']
            suffix_table = basename(source_path.rstrip('/'))
            autogen_table_name = source_table + suffix_table.replace('.', '_')
            #print(f'Replacing {source_table} with {new_table_name}')
            #configs['sql_query'] = configs['sql_query'].replace(
            #    source_table,
            #    new_table_name
            #)
            #print(f'After replacement SQL:\n{configs["sql_query"]}')

            job_name = f'{configs["job_name"]}_{source_table}'

            # Create and start crawler
            crawler_name = DagHandler.create_crawler(
                job_name,
                source_path,
                source_table,
                crawler_role_arn,
                autogen_table_name
            )
        print(f'After replacement SQL:\n{configs["sql_query"]}')

        # Create the airflow DAG
        DagHandler.create_dag_from_template(configs)

    @staticmethod
    def create_crawler(
            job_name,
            source_path,
            source_table,
            crawler_role_arn,
            autogen_table_name
    ):
        crawler_name = job_name + '_crawler'
        try:
            resp = DagHandler.glue_client.delete_crawler(Name=crawler_name)
        except Exception as e:
            pass

        resp = DagHandler.glue_client.create_crawler(
            Name = crawler_name,
            DatabaseName = 'default',
            Role = crawler_role_arn,
            Targets = {'S3Targets': [{'Path': source_path}]},
            TablePrefix = source_table,
            SchemaChangePolicy = {
                'UpdateBehavior': 'UPDATE_IN_DATABASE',
                'DeleteBehavior': 'LOG'
            }
        )
        resp = DagHandler.glue_client.start_crawler(Name=crawler_name)
        DagHandler.wait_for_crawler_ready(crawler_name)
        DagHandler.rename_table(autogen_table_name, source_table)
        return crawler_name

    @staticmethod
    def rename_table(old_name, new_name):
        database = 'default'
        resp = DagHandler.glue_client.get_table(DatabaseName=database, Name=old_name)
        table_input = response['Table']
        table_input['Name'] = new_name
        table_input.pop('CreatedBy')
        table_input.pop('CreateTime')
        table_input.pop('UpdateTime')
        table_input.pop('DatabaseName')
        resp2 = DagHandler.glue_client.create_table(DatabaseName=database, TableInput=table_input)
        print(f'Response to create new table {resp2}')

    @staticmethod
    def create_dag_from_template(configs):
        dags_dir = os.getcwd() + '/dags'
        dag_name = configs['job_name'] + '_dag'

        with open(f'{dags_dir}/template_dag.py', 'r') as f:
            content = f.read()
    
        content = DagHandler.customize_dag(dag_name, content, configs)

        print('Creating file with content:\n', content)

        with open(f'{dags_dir}/{dag_name}.py', 'w') as f:
            f.write(content)

    @staticmethod
    def customize_dag(dag_name, content, configs):
        substitutions = {
            'template_dag = True': 'template_dag = False',
            'placeholder_dag': dag_name,
            'placeholder_cron': configs['cron_expr'],
            'placeholder_task': configs['job_name'] + '_task',
            'placeholder_sql': configs['sql_query'],
            'placeholder_template': DagHandler.template,
            'placeholder_partitions': str(configs['partitions']),
            'placeholder_public_subnet': configs['public_subnet_id'],
            'placeholder_private_subnet': configs['private_subnet_id'],
            'placeholder_security_group': configs['superserver_security_group'],
            'placeholder_table': configs['destination_table'],
            'placeholder_logs_path': configs['logs_path'],
            'placeholder_master_sg': configs['master_security_group'],
            'placeholder_slave_sg': configs['slave_security_group'],
            'placeholder_destination_path': configs['destination_path'],
            'placeholder_service_access_sg': configs['service_access_sg']
        }

        for k, v in substitutions.items():
            content = content.replace(k, v)

        return content

    @staticmethod
    def wait_for_crawler_ready(crawler_name):
        ready = False
        print('Waiting for crawler to become available...')
        while not ready:
            resp = DagHandler.glue_client.get_crawler(Name=crawler_name)
            state = resp['Crawler']['State']
            ready = (state == 'READY')
            time.sleep(0.5)
        print('Done')
