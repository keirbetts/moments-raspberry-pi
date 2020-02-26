
import boto3
import threading
import os
from utils import getUsrPhotoUrls, downloadPhotos, slideControl


def start():
    # start slide show
    os.system('sh feh_stock.sh')


previousUrls = []
stock = True


def main():
    global previousUrls
    global stock
    # os.system('sh feh_stock.sh')
    threading.Timer(10.0, main).start()
    print('INSIDE MAIN')

    # get photo urls
    currentUrls = getUsrPhotoUrls()

    # if len(previousUrls) != len(currentUrls):
    if sorted(set(previousUrls)) != sorted(set(currentUrls)):
        # download photos
        downloadPhotos(previousUrls, currentUrls)
        stock = downloadPhotos(previousUrls, currentUrls)
        previousUrls = getUsrPhotoUrls()
        print(stock)

        slideControl(stock)


start()
main()
