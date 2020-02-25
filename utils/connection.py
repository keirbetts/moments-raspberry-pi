import boto3


def dbConnection():
    client = boto3.resource('dynamodb')
