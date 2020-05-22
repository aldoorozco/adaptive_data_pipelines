from clients import Clients
from storage import Storage
from os.path import basename, dirname
from multiprocessing import Pool

import requests
import re
import json
import time
import os

class DagHandler:
    glue_client = Clients.glue_client
    template = None

    def __init__(self):
        storage = Storage()
        templates_bucket = 'abdp-templates'
        folder = 'spark'
        DagHandler.template = storage.copy_bucket(
             '/app/template/target/tog-0.1.jar',
             templates_bucket,
             folder
        )

    @staticmethod
    def run(configs):
        configs['sql_query'] = configs['sql_query'].lower().replace('\n', ' ')

        source_count = int(configs['source_count'])

        crawler_role_arn = configs['crawler_role_arn']

        crawlers = []
        for i in range(1, source_count + 1):
            source_path = configs[f'source{i}_path']
            source_table = configs[f'source{i}_table']
            job_name = f'{configs["job_name"]}_{source_table}'

            # Create and start crawler
            crawler_name = DagHandler.create_crawler(
                job_name,
                source_path,
                source_table,
                crawler_role_arn
            )

            crawlers.append(crawler_name)

        for c in crawlers:
            DagHandler.wait_for_crawler_ready(c)

        # Create the airflow DAG
        DagHandler.create_dag_from_template(configs)

    @staticmethod
    def create_crawler(
            job_name,
            source_path,
            source_table,
            crawler_role_arn
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
            Targets = {'S3Targets': [{'Path': dirname(source_path)}]},
            TablePrefix = '',
            SchemaChangePolicy = {
                'UpdateBehavior': 'UPDATE_IN_DATABASE',
                'DeleteBehavior': 'LOG'
            }
        )
        resp = DagHandler.glue_client.start_crawler(Name=crawler_name)
        return crawler_name

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
        print(f'Waiting for {crawler_name} to become ready...')
        while not ready:
            resp = DagHandler.glue_client.get_crawler(Name=crawler_name)
            state = resp['Crawler']['State']
            ready = (state == 'READY')
            time.sleep(0.5)
        print(f'Done {crawler_name}')
