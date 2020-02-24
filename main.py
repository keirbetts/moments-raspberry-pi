
import urllib.request
import boto3

# make connection to dynamo db
client = boto3.resource('dynamodb')

# connect to table
table = client.Table("Moments-dev")

# get urls
response = table.get_item(
    Key={"usr": "crookydan"}
)

pictureUrls = response["Item"]["picURL"]


# iterate through and dl photos
counter = 0
for url in pictureUrls:
    print(url)
    counter += 1
    urllib.request.urlretrieve(
        url, "/home/domh/Pictures/temp/{}.jpg".format(counter))


# contact db and get list of all urls from db
# AWS sdk - boto3
# target attribute picURL
# iterate over list and get urls
# download each url to folder

# show images thorugh FEH
