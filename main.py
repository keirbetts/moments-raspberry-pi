
import boto3
import threading
from utils import getUsrPhotoUrls, downloadPhotos


previousUrls = []


def main():
    global previousUrls
    threading.Timer(10.0, main).start()

    # get photo urls
    currentUrls = getUsrPhotoUrls()
    print(currentUrls)

    # download photos
    downloadPhotos(previousUrls, currentUrls)
    previousUrls = getUsrPhotoUrls()


main()
