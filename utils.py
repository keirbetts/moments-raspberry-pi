import urllib.request
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


def downloadPhotos(previousUrls, currentUrls):
    if len(previousUrls) != len(currentUrls):
        counter = 0
        for url in currentUrls:
            # print(url)
            counter += 1
            urllib.request.urlretrieve(
                url, "/home/domh/Pictures/temp/{}.jpg".format(counter))
