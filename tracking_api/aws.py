"""
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
"""

import os
import json
import configparser

import boto3
from botocore.exceptions import ClientError

from .config import ConfigHandler


class AwsStorageMgmt:
    def __init__(self):
        # self.s3_resour = boto3.resource("s3")
        self.s3_client = boto3.client("s3")
        self.config = ConfigHandler(project_name="tracking-api")
        if self.config.check_config_exists():
            self.configs = self.config.get_configs()
            self.bucket = self.configs.get("aws_bucket", None)
            self.object_prefix = self.configs.get("object_prefix", None)
        else:
            print("config file does not exist, run `mmgmt configure`")

    def upload_json(self, object_name: str, file_path: str):
        """
        Upload an object to an Amazon S3 bucket using an AWS SDK
        https://docs.aws.amazon.com/AmazonS3/latest/userguide/example_s3_PutObject_section.html
        """
        # print(self.object_prefix,self.bucket, object_name)
        object_name = os.path.join(self.object_prefix, object_name)
        try:
            # print(f'upload to s3://{self.bucket}/{object_name}')
            with open(file_path, "rb") as data:
                self.s3_client.upload_fileobj(data, self.bucket, object_name)
        except ClientError as e:
            print(e)
            return False
        return True


aws = AwsStorageMgmt()
