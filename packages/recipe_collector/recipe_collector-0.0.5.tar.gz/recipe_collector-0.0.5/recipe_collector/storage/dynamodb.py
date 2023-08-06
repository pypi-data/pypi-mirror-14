import boto3
from recipe_collector.utils.decorators import coroutine


@coroutine
def urls_dynamodb(table_name, aws_access_key, aws_secret_key, aws_region):
    """
    This coroutine receives tuples of title and url values and saves them to AWS DynamoDB.
    """
    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region)
    table = session.resource('dynamodb').Table(table_name)
    while True:
        source_url = yield
        table.put_item(Item={
            'url': source_url
        })


@coroutine
def html_dynamodb(table_name, aws_access_key, aws_secret_key, aws_region):
    """
    This coroutine receives tuples of url and HTML values and saves them to AWS DynamoDB.
    """
    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region)
    table = session.resource('dynamodb').Table(table_name)
    while True:
        source_url, html = yield
        table.put_item(Item={
            'url': source_url,
            'html': html
        })
