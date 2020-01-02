from os.path import basename
from clients import Clients
import boto3
import botocore
import time

class Storage:
    def __init__(self):
        self.s3_client = Clients.s3_client

    def file_exists(self, bucket, key):
        s3 = boto3.resource('s3')
        exists = True

        try:
            s3.Object(bucket, key).load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
               exists = False
        return exists

    def copy_bucket(self, file_path, bucket, key):
        full_key = f'{key}/{basename(file_path)}'

        if self.file_exists(bucket, full_key):
            print(f'Skipping file copy {file_path}, as it already exists')
        else:
            print(f'[INFO] Copying {file_path} to bucket {bucket}...')
            start = time.time()
            with open(file_path, 'rb') as data:
                self.s3_client.put_object(Bucket=bucket, Key=full_key, Body=data)
            end = time.time()
            diff = end - start
            print(f'[INFO] Operation took {diff:.2f} seconds')

        return f's3://{bucket}/{full_key}'
