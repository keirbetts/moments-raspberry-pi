
import boto3
import threading
import os
from utils import getUsrPhotoUrls, downloadPhotos, slideControl


previousUrls = []
stock = True


def start():
    # start slide show
    os.system('sh feh_stock.sh')


def main():
    global previousUrls
    global stock
    threading.Timer(10.0, main).start()

    # get photo urls
    currentUrls = getUsrPhotoUrls()

    if sorted(set(previousUrls)) != sorted(set(currentUrls)):
        # download photos
        downloadPhotos(previousUrls, currentUrls)
        stock = downloadPhotos(previousUrls, currentUrls)
        previousUrls = getUsrPhotoUrls()

        slideControl(stock)


start()
main()
