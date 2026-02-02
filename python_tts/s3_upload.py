import logging
import boto3
from botocore.exceptions import ClientError
import os


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)
    # set up session to use TD_DEV profile under ~/.aws/credentials for testing
    boto3.setup_default_session(profile_name="s3Profile")

    # Upload the file and enforce content-type of audio/mpeg, else it defaults to audio/mp3
    s3_client = boto3.client("s3")
    try:
        response = s3_client.upload_file(
            file_name, bucket, object_name, ExtraArgs={"ContentType": "audio/mpeg"}
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True
