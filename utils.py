import urllib.request
import boto3
import shutil
import os

counter = 0


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
    global counter
    additionalUrls = list(set(currentUrls) - set(previousUrls))
    additionalTotal = len(currentUrls) - len(previousUrls)

    if additionalTotal > 0:
        print('ADDITIONAL URLS COMPARISON')
        for url in additionalUrls:
            print(url, 'INSIDE THE FOR LOOP')
            counter += 1
            urllib.request.urlretrieve(
                url, "/home/domh/Pictures/temp/{}.jpeg".format(counter))
        return False
    elif additionalTotal == 0:
        return
    else:
        # deletion functionality
        return True


def slideControl(stock):
    if stock:
        print("killing slideshow")
        os.system('sh kill.sh')
        os.system('sh feh_stock.sh')
    elif stock == False:
        print("killing slid show, starting stock")
        os.system('sh kill.sh')
        os.system('sh script_slideshow.sh')
