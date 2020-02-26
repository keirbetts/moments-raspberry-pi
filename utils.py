import urllib.request
import boto3
import shutil
import os

counter = 0
lib = {}


def getUsrPhotoUrls():
    client = boto3.resource('dynamodb')
    # connect to table
    table = client.Table("Moments-dev")

    response = table.get_item(
        Key={"usr": "crookydan"}
    )
    pictureUrls = response["Item"]["picURL"]

    return pictureUrls


def downloadPhotos(previousUrls, currentUrls):
    global counter
    additionalTotal = len(currentUrls) - len(previousUrls)

    if len(os.listdir('/home/pi/Pictures/temp')) == 0:
        # download all current urls
        return addPhotosToStorage(list(currentUrls))
    elif additionalTotal > 0:
        return addPhotosToStorage(list(set(currentUrls) - set(previousUrls)))
    else:
        return deletePhotosFromStorage(list(set(previousUrls) - set(currentUrls)))


def slideControl(stock):
    if stock:
        os.system('sh kill.sh')
        os.system('sh feh_stock.sh')
    elif stock == False:
        os.system('sh kill.sh')
        os.system('sh script_slideshow.sh')


def addPhotosToStorage(additionalUrls):
    global counter
    global lib
    for url in additionalUrls:
        counter += 1
        urllib.request.urlretrieve(
            url, "/home/domh/Pictures/temp/{}.jpeg".format(counter))
        lib[url] = counter
    return False


def deletePhotosFromStorage(additionalUrls):
    global lib
    for url in additionalUrls:
        os.remove("/home/pi/Pictures/temp/{}.jpeg".format(lib[url]))
        del lib[url]

    if len(os.listdir('/home/pi/Pictures/temp')) == 0:
        return True
    else:
        return False
