import boto3


def getUsrPhotoUrls():
    client = boto3.resource('dynamodb')
    # connect to table
    table = client.Table("Moments-dev")

    response = table.get_item(
        Key={"usr": "test"}
    )
    pictureUrls = response["Item"]["picURL"]

    return pictureUrls
