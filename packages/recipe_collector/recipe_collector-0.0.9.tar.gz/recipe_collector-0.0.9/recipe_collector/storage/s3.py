from uuid import uuid4
import boto3
from recipe_collector.utils.decorators import coroutine


@coroutine
def html_s3(bucket_name, aws_access_key, aws_secret_key, aws_region):
    """
    This coroutine receives tuples of url and HTML values and saves to S3.

    Args:
    * bucket_name: An S3 bucket name
    * aws_access_key: An AWS access key
    * aws_secret_key: An AWS secret key
    * aws_region: An AWS region
    """
    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region)
    bucket = session.resource('s3').Bucket(bucket_name)
    while True:
        source_url, html = yield
        bucket.put_object(
            ACL='private',
            Body=html.encode('utf-8'),
            Key=uuid4().hex,
            Metadata={
                'url': source_url
            }
        )
