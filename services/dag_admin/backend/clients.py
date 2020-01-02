import boto3

class Clients:
    s3_client = boto3.client('s3', region_name='us-east-1')
    glue_client = boto3.client('glue', region_name='us-east-1')

    def __init__(self):
        pass
