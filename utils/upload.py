import boto3
import uuid

from django.conf import settings


class FileUploader:

    def __init__(
            self, aws_key=settings.AWS_SERVER_PUBLIC_KEY,
            aws_secret=settings.AWS_SERVER_SECRET_KEY,
            aws_region=settings.AWS_REGION):
        self._s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret,
            region_name=aws_region,
        )

    def upload_file_to_s3(
            self, local_filename, s3_bucket=settings.AWS_S3_BUCKET_NAME,
            remote_filename=None):
        if not remote_filename:
            remote_filename = str(uuid.uuid4())
        self._s3.upload_file(local_filename, s3_bucket, remote_filename)
