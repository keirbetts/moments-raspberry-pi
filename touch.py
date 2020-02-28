import os
from time import sleep
import RPi.GPIO as GPIO
#from main import start

GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    if(GPIO.input(21) == True):
        print("Hello Wold")
        sleep(0.2);
        

    