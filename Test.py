#coding:UTF-8

import RPi.GPIO as GPIO
import dht11
import time
import datetime
from twython import Twython

import TwitterAccess
import ImageCapture

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

dht11Inst = dht11.DHT11(pin=4)

dateTimeFormat = "%Y/%m/%d %H:%M:%S"
filePath = '/usr/app/niwashi/img/capture.jpg'

twitter = TwitterAccess.TwitterAccess()
capt = ImageCapture.ImageCapture()

loopContinue = True

while loopContinue:
    sleepTime = 60
    
    current_time = datetime.datetime.now().strftime(dateTimeFormat)

    loopRead = True
    
    while loopRead:
        dht11Read = dht11Inst.read()
        
        if dht11Read.is_valid():
            textTweet = 'ゲンザイノ ニチジハ ' + current_time + ' キオン ' + str(dht11Read.temperature) + '℃ ' + 'シツド ' + str(dht11Read.humidity) + '% デス.'
            
            if capt.putImage(filePath):
                twitter.tweetImage(textTweet, filePath)
            else:
                twitter.tweet(textTweet)
            
            print('success tweeted.')
            
            loopRead = False
            
        else:
            print('dht11 error')
            time.sleep(1)

    time.sleep(sleepTime)

