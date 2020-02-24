
import urllib.request
import boto3
import threading

# make connection to dynamo db

newUrlCount = 0


def getUrls():
    global newUrlCount
    threading.Timer(10.0, getUrls).start()
    client = boto3.resource('dynamodb')

    # connect to table
    table = client.Table("Moments-dev")

    # get urls
    response = table.get_item(
        Key={"usr": "crookydan"}
    )

    # iterate through and dl photos

    pictureUrls = response["Item"]["picURL"]

    print(len(pictureUrls))

    if(newUrlCount != len(pictureUrls)):
        counter = 0
        newUrlCount = len(pictureUrls)
        for url in pictureUrls:
            print(url)
            counter += 1
            urllib.request.urlretrieve(
                url, "/home/domh/Pictures/temp/{}.jpg".format(counter))


getUrls()

# contact db and get list of all urls from db
# AWS sdk - boto3q
# target attribute picURL
# iterate over list and get urls
# download each url to folder

# show images thorugh FEH
