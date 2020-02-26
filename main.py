
import boto3
import threading
import os
from utils import getUsrPhotoUrls, downloadPhotos, slideControl, initDownload


previousUrls = []
stock = True


def start():
    global previousUrls
    # start slide show
    os.system('sh feh_stock.sh')
    previousUrls = initDownload()
    if len(previousUrls) > 0:
        slideControl(False)


def main():
    global previousUrls
    global stock
    threading.Timer(2.0, main).start()

    # get photo urls
    currentUrls = getUsrPhotoUrls()
    print(sorted(set(previousUrls)) != sorted(set(currentUrls)))

    if sorted(set(previousUrls)) != sorted(set(currentUrls)):
        # download photos
        stock = downloadPhotos(previousUrls, currentUrls)
        previousUrls = currentUrls

        slideControl(stock)


start()
main()
