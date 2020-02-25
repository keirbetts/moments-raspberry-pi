import boto3


def dbConnection():
    client = boto3.resource('dynamodb')
    # connect to table
    table = client.Table("Moments-dev")
    return table
