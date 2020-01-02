from boto3.s3.transfer import TransferConfig
from os.path import basename
from clients import Clients
import threading
import time
import boto3
import botocore
import os
import sys

class ProgressPercentage:
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()

class Storage:
    def __init__(self):
        self.s3 = boto3.resource('s3')

    def file_exists(self, bucket, key):
        s3 = boto3.resource('s3')
        exists = True

        try:
            s3.Object(bucket, key).load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
               exists = False 
        return exists

    def multi_part_copy(self, file_path, bucket, key):
        # Multipart upload
        full_key = f'{key}/{basename(file_path)}'
        if self.file_exists(bucket, full_key):
            print(f'Skipping file copy {file_path}, as it already exists')
        else:
            cpus = len(os.sched_getaffinity(0)) * 2
            print(f'[INFO] Copying {file_path} to bucket {bucket} with {cpus} threads...')
            start = time.time()
            config = TransferConfig(
                multipart_threshold=1024 * 25,
                max_concurrency=cpus,
                multipart_chunksize=1024 * 25,
                use_threads=True
            )
            self.s3.meta.client.upload_file(
                file_path, bucket, full_key,
                ExtraArgs={'ACL': 'private'},
                Config=config,
                Callback=ProgressPercentage(file_path)
            )
            end = time.time()
            diff = end - start
            print(f'[INFO] Operation took {diff:.2f} seconds')
        return f's3://{bucket}/{full_key}'

    def copy_bucket(self, file_path, bucket, key):
        full_key = f'{key}/{basename(file_path)}'
        print(f'[INFO] Copying {file_path} to bucket {bucket}...')
        start = time.time()
        with open(file_path, 'rb') as data:
            self.s3_client.put_object(Bucket=bucket, Key=full_key, Body=data)
        end = time.time()
        diff = end - start
        print(f'[INFO] Operation took {diff:.2f} seconds')
        return f's3://{bucket}/{full_key}'
