from time import sleep

import boto3
import requests

class Cluster:
    client = boto3.client('emr', region_name='us-east-1')
    master_instance_type = 'm5.xlarge'
    emr_version = 'emr-5.29.0'
    ec2_key_name = 'deploy'
    partitions_per_core = 10

    def __init__(self):
        pass

    @staticmethod
    def calculate_settings(partitions):
        settings = {
            'executors': str(int((int(partitions) / Cluster.partitions_per_core) + 1)),
            'cores': '6',
            'memory': '11G',
            'instance_type': 'm5.2xlarge'
        }
        return settings

    @staticmethod
    def create(
        name,
        template_path,
        sql,
        partitions,
        subnet_id,
        destination_table,
        logs_path,
        security_group_master,
        security_group_slave,
        destination_path,
        service_access_sg
    ):
        settings = Cluster.calculate_settings(partitions)
        print(f'Received cluster creation request with the following settings {settings}')
        sql_query = sql.replace('\n', ' ')\
                        .replace('`', '\`')

        step_args = ['spark-submit',
                     '--deploy-mode', 'cluster',
                     '--master', 'yarn',
                     '--class', 'com.tog.template.Main',
                     '--num-executors', settings['executors'],
                     '--conf', f'spark.sql.shuffle.partitions={partitions}',
                     template_path,
                     sql_query, destination_table,
                     destination_path]
        app_names = ['spark', 'hive']
        apps = [dict(Name=x) for x in app_names]

        mongo_server_ip = requests.get('https://api.ipify.org').text

        print(f'Submitting job with {" ".join(step_args)}')
        resp = Cluster.client.run_job_flow(
            Name = name + '_cluster',
            LogUri = logs_path,
            ReleaseLabel = Cluster.emr_version,
            Instances = {
                'MasterInstanceType': Cluster.master_instance_type,
                'SlaveInstanceType': settings['instance_type'],
                'InstanceCount': int(settings['executors']),
                'KeepJobFlowAliveWhenNoSteps': False,
                'TerminationProtected': False,
                'Ec2SubnetId': subnet_id,
                'Ec2KeyName': Cluster.ec2_key_name,
                'EmrManagedMasterSecurityGroup': security_group_master,
                'EmrManagedSlaveSecurityGroup': security_group_slave,
                'ServiceAccessSecurityGroup': service_access_sg
            },
            Steps = [{
                'Name': 'ETLCustomQuery',
                'ActionOnFailure': 'TERMINATE_CLUSTER',
                'HadoopJarStep': {
                    #This is a generic JAR for python scripts
                    'Jar': 'command-runner.jar',
                    'Args': step_args
                }
            }],
            Configurations=[
            {
                'Classification': 'core-site',
                'Properties': {
                  'spline.mode': 'BEST_EFFORT',
                  'spline.persistence.factory': 'za.co.absa.spline.persistence.mongo.MongoPersistenceFactory',
                  'spline.mongodb.url': f'mongodb://{mongo_server_ip}/spline'
                }
            },
            {
                'Classification': 'hive-site',
                'Properties': {
                  'hive.metastore.client.factory.class': 'com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory',
                  'hive.exec.dynamic.partition': 'true',
                  'hive.exec.dynamic.partition.mode': 'nonstrict',
                  'hive.input.format': 'org.apache.hadoop.hive.ql.io.CombineHiveInputFormat'
                }
            },
            {
                'Classification': 'spark',
                'Properties': {
                  'maximizeResourceAllocation': 'true'
                }
            }
            ],
            Tags=[
            {
                'Key': 'Name',
                'Value': 'EMR instance'
            }
            ],
            Applications = apps,
            JobFlowRole='EMR_EC2_DefaultRole',
            ServiceRole='EMR_DefaultRole'
        )

        status_code = int(resp['ResponseMetadata']['HTTPStatusCode'])
        if status_code != 200:
            raise Exception('[ERROR] Failed creating cluster')

        print('[INFO] Successfully started cluster. Waiting for it to terminate...')
        cluster_arn = resp['ClusterArn']
        resp = Cluster.client.list_clusters()
        if status_code != 200:
            raise Exception('[ERROR] Reading clusters list')

        cluster_id = None
        for cluster in resp['Clusters']:
            if cluster['ClusterArn'] == cluster_arn:
                cluster_id = cluster['Id']

        cluster_done = False

        while not cluster_done:
            sleep(500)
            resp = Cluster.client.describe_cluster(ClusterId=cluster_id)
            if status_code != 200:
                raise Exception(f'[ERROR] Describing cluster {cluster_id}')
            print('Describe cluster output', resp)
            cluster_state = resp['Cluster']['Status']['State']
            if cluster_state == 'TERMINATED' or cluster_state == 'TERMINATED_WITH_ERRORS':
                cluster_done = True

        if cluster_state == 'TERMINATED_WITH_ERRORS':
            err = resp['Cluster']['Status']['StateChangeReason']['Message']
            print(f'[ERROR] Cluster terminated with errors: {err}')
            exit(1)
