import cv2
import time
import os
import sys
import boto3
import re
from picamera.array import PiRGBArray
from picamera import PiCamera

import os
from time import sleep
import RPi.GPIO as GPIO
#from main import start

GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)


faceClient = boto3.client('rekognition')
s3Client = boto3.client("s3")
dynamoClient = boto3.resource("dynamodb")


def runpicam():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.1)

    faceCascade = cv2.CascadeClassifier(
        "/home/pi/face-recognition/haarcascade.xml")

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        image = frame.array
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #cv2.imshow("Image", image)
        if key == ord("q"):
            break

        if len(faces) > 0:
            # if face is detected save the image to file
            detected = True
            img_name = "captured_face.png"
            path = "/home/pi/face-recognition/Images"
            cv2.imwrite(os.path.join(path, img_name), image)
            camera.stop_preview()
            camera.close()

            return True
        else:
            camera.stop_preview()
            camera.close()
            return False
           # Draw a rectangle around the faces


def uploadToS3():
    # upload web cam footage to s3
    for root, dirs, files in os.walk("/home/pi/face-recognition/Images"):
        for file in files:
            s3Client.upload_file(os.path.join(root, file),
                                 "face-recogonition", file)  # note this is the spelling on S3


def getAllFaces():
    faceList = []
    bucket = s3Client.list_objects_v2(Bucket="face-recogonition")
    for obj in bucket["Contents"]:
        faceList.append(obj["Key"])

    faceRef = filter(lambda item: "reference" in item, faceList)
    return faceRef


def runFaceCompare():
    referenceList = list(getAllFaces())
    verified = ""

    count = len(referenceList)

    for ref in referenceList:
        response = faceClient.compare_faces(
            SourceImage={
                # "Bytes": b'bytes',
                "S3Object": {
                    "Bucket": "face-recogonition",
                    "Name": ref
                }
            },
            TargetImage={
                # "Bytes": b'bytes',
                "S3Object": {
                    "Bucket": "face-recogonition",
                    "Name": "captured_face.png"
                }
            },
            SimilarityThreshold=70.0
        )

        # get confidence
        confidence = 0

        if len(response["FaceMatches"]) != 0:
            confidence = response["FaceMatches"][0]["Similarity"]

        if (confidence > 90):
            setActiveUser(ref)
            os.system('sh kill.sh')
            os.system('sh script_slideshow.sh')
            return True
        else:
            count -= 1

        if count == 0:
            return False


# runFaceCompare()
def setActiveUser(ref):

    user = re.match(r"(.*?)-", ref).group(1)

    print(user)

    table = dynamoClient.Table("Moments-dev")

    setActiveUser = table.update_item(
        Key={"usr": "Active"},
        UpdateExpression="SET refActive = :val",
        ExpressionAttributeValues={
            ":val": user,
        },
        ReturnValues="UPDATED_NEW"
    )


def start():

    faceDetected = runpicam()
    if faceDetected:
        uploadToS3()
        runFaceCompare()
    else:
        print("sorry couldn't verify your face")


while True:
    if(GPIO.input(21) == True):
        start()
        sleep(0.2)
