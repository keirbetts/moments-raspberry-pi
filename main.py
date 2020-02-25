
import boto3
import threading
import os
from utils import getUsrPhotoUrls, downloadPhotos


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

        print(len(currentUrls))
        if stock:
            print("killing slideshow")
            os.system('sh kill.sh')
            os.system('sh feh_stock.sh')
        elif stock == False:
            print("killing slid show, starting stock")
            os.system('sh kill.sh')
            os.system('sh script_slideshow.sh')


start()
main()
