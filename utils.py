import urllib.request
import boto3


def getUsrPhotoUrls():
    client = boto3.resource('dynamodb')
    # connect to table
    table = client.Table("Moments-dev")

    response = table.get_item(
        Key={"usr": "crookydan"}
    )
    pictureUrls = response["Item"]["picURL"]

    return pictureUrls


# def downloadPhotos(previousUrls, currentUrls):
#     if len(previousUrls) != len(currentUrls):
#         counter = 0
#         for url in currentUrls:
#             # print(url)
#             counter += 1
#             urllib.request.urlretrieve(
#                 url, "/home/domh/Pictures/temp/{}.jpg".format(counter))


# previousUrls = set(["url1", "url2", "url3", "url4"])
# currentUrls = set(["url1", "url2", "url3", "url4", "url5", "url6", "url7"])

counter = 0


def downloadPhotos(previousUrls, currentUrls):
    global counter
    additionalUrls = list(set(currentUrls) - set(previousUrls))
    print(additionalUrls)
    if len(previousUrls) != len(currentUrls):
        if(len(additionalUrls) > 0):
            print(additionalUrls)

            for url in additionalUrls:
                counter += 1
                urllib.request.urlretrieve(
                    url, "/home/domh/Pictures/temp/{}.jpg".format(counter))
