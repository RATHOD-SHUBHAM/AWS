import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os

class sts_client:
    def __init__(self) -> None:
        load_dotenv()

        self.ACCESS_KEY = os.environ.get('ACCESS_KEY')
        self.SECRET_KEY = os.environ.get('SECRET_KEY')


    def assume_role(self, assume_role_arn, session_name):
        """
        Assumes a role that grants permission to list the Amazon S3 buckets in the account.
        Uses the temporary credentials from the role to list the buckets that are owned
        by the assumed role's account.

        :param user_key: The access key of a user that has permission to assume the role.
        :param assume_role_arn: The Amazon Resource Name (ARN) of the role that
                                grants access to list the other account's buckets.
        :param session_name: The name of the STS session.
        """
        sts_client = boto3.client(
                'sts', 
                aws_access_key_id=self.ACCESS_KEY, 
                aws_secret_access_key=self.SECRET_KEY
            )
        try:
            response = sts_client.assume_role(
                    RoleArn=assume_role_arn, 
                    RoleSessionName=session_name,
                    DurationSeconds=3600
                )
            temp_credentials = response['Credentials']
            print(f"Assumed role {assume_role_arn} and got temporary credentials.")
        
        except ClientError as error:
            print(f"Couldn't assume role {assume_role_arn}. Here's why: "
                f"{error.response['Error']['Message']}")
            raise

        # Create an S3 resource that can access the account with the temporary credentials.
        s3_resource = boto3.resource(
                's3',
                aws_access_key_id=temp_credentials['AccessKeyId'],
                aws_secret_access_key=temp_credentials['SecretAccessKey'],
                aws_session_token=temp_credentials['SessionToken']
            )
        print(f"Listing buckets for the assumed role's account:")

        return s3_resource