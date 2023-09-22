import boto3
from botocore.exceptions import ClientError
import os
import logging
from sts_client import sts_client


def list_buckets_from_assumed_role(s3_resource):
    """
    Assumes a role that grants permission to list the Amazon S3 buckets in the account.
    Uses the temporary credentials from the role to list the buckets that are owned
    by the assumed role's account.

    :param user_key: The access key of a user that has permission to assume the role.
    :param assume_role_arn: The Amazon Resource Name (ARN) of the role that
                            grants access to list the other account's buckets.
    :param session_name: The name of the STS session.
    """
    
    try:
        for bucket in s3_resource.buckets.all():
            print(bucket.name)
        
    
    except ClientError as error:
        print(f"Couldn't list buckets for the account. Here's why: "
              f"{error.response['Error']['Message']}")
        raise



def create_bucket_from_assumed_role(s3_resource, bucket_name, AWS_REGION = None):
    """
    Assumes a role that grants permission to list the Amazon S3 buckets in the account.
    Uses the temporary credentials from the role to list the buckets that are owned
    by the assumed role's account.

    :param user_key: The access key of a user that has permission to assume the role.
    :param assume_role_arn: The Amazon Resource Name (ARN) of the role that
                            grants access to list the other account's buckets.
    :param session_name: The name of the STS session.
    """
    
    try:
        if AWS_REGION is None:
            bucket = s3_resource.create_bucket(
                Bucket=bucket_name
            )
        else:

            location = {'LocationConstraint': AWS_REGION}
            bucket = s3_resource.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration=location
                )
        
        print("Amazon S3 bucket has been created")
        
    
    except ClientError as error:
        print(f"Couldn't create buckets for the account. Here's why: "
              f"{error.response['Error']['Message']}")
        raise




def upload_file_from_assumed_role(s3_resource, file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)


    try:
        response = s3_resource.meta.client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file_from_assumed_role(s3_resource, file_name, bucket, object_name):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    try:
        response = s3_resource.meta.client.download_file(bucket, object_name, file_name)
        
    except ClientError as e:
        logging.error(e)
        return False
    return True

def list_content_file_from_assumed_role(s3_resource, bucket):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    try:
        s3_bucket = s3_resource.Bucket(bucket)
        print('Listing Amazon S3 Bucket objects/files:')

        for obj in s3_bucket.objects.all():
            print(f'-- {obj.key}')
        
    except ClientError as e:
        logging.error(e)
        return False
    return True

def delete_file_from_assumed_role(s3_resource, bucket, key_name):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    try:
        s3_resource.meta.client.delete_object(Bucket=bucket, Key=key_name)
        
    except ClientError as e:
        logging.error(e)
        return False
    return True

def delete_s3_from_assumed_role(s3_resource, bucket):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    try:
        s3_resource.meta.client.delete_bucket(Bucket=bucket)
        
    except ClientError as e:
        logging.error(e)
        return False
    return True



if __name__ == '__main__':

    # sts client connetion
    RoleArn='Replace with your ARN'
    session_name = 'AssumeRoleDemoSession'
    sts_obj = sts_client()
    s3_resource = sts_obj.assume_role(RoleArn, session_name)

    # List all the Bucket
    list_buckets_from_assumed_role(s3_resource)

    # Create a Bucket
    # AWS_REGION = "us-east-1" # if us-east-1 we dont have to pass this parameter
    # bucket_name = "fastapitestbucket1"
    # create_bucket_from_assumed_role(s3_resource, bucket_name)


    ## Upload a file to bucket

    # bucket_name = "fastapitestbucket1"
    # file_name = "/home/ubuntu/AWS/upload/test-2.jpg"
    # object_name=None

    # result_upload = upload_file_from_assumed_role(s3_resource, file_name, bucket_name, object_name)
    # if result_upload :
    #     print("bucket file uploaded successfully..!")
    # else:
    #     print("bucket file upload failed..!")


    ## Download a file from bucket

    # bucket_name = "fastapitestbucket1"
    # file_path = "/home/ubuntu/AWS/downloaded_data/test-2.jpg"
    # object_name="test-2.jpg"

    # result_download = download_file_from_assumed_role(s3_resource, file_path, bucket_name, object_name)
    # if result_download :
    #     print("bucket file downloaded successfully..!")
    # else:
    #     print("bucket file download failed..!")


    ## List all the content of file
    # bucket_name = "fastapitestbucket1"
    # list_content_file_from_assumed_role(s3_resource, bucket_name)

    ## Delete a file from bucket
    # bucket_name = "fastapitestbucket1"
    # key_name = "test-2.jpg"
    # result_delete = delete_file_from_assumed_role(s3_resource, bucket_name, key_name)
    # if result_delete :
    #     print("bucket file deleted successfully..!")
    # else:
    #     print("bucket file delete failed..!")


    ## Delete bucket
    # bucket_name = "fastapitests1"
    # result_deletebucket = delete_s3_from_assumed_role(s3_resource, bucket_name)
    # if result_deletebucket :
    #     print("bucket deleted successfully..!")
    # else:
    #     print("bucket delete failed..!")