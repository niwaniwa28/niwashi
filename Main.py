#coding:UTF-8

import RPi.GPIO as GPIO
import dht11
import time
import datetime
import os
import subprocess

from twython import Twython

import TwitterAccess
import ImageCapture

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

dht11Inst = dht11.DHT11(pin=4)

dateTimeFormat = "%Y/%m/%d %H:%M:%S"
#script_dir = os.path.dirname(os.path.abspath(__file__))
#filePath = os.path.join(script_dir, '/img/capture.jpg')
filePath = '/usr/app/niwashi/img/capture.jpg'

twitter = TwitterAccess.TwitterAccess()
capt = ImageCapture.ImageCapture()

powerOnCmd = "sudo python /usr/app/hub_ctrl.py -h 0 -P 1 -p 1"
powerOffCmd = "sudo python /usr/app/hub_ctrl.py -h 0 -P 1 -p 0"

errorCnt = 0
loopContinue = True

while loopContinue:
    sleepTime = 3600
    
    clockTimeH = datetime.datetime.now().strftime('%H')
    clockTimeM = datetime.datetime.now().strftime('%M')
    
    if clockTimeM > "30":
        sleepTime = 1800
    
    if clockTimeH == "01" or clockTimeH == "08" or clockTimeH == "11" or clockTimeH == "14" or clockTimeH == "17":
    
        current_time = datetime.datetime.now().strftime(dateTimeFormat)

        loopRead = True
        
        while loopRead:
            dht11Read = dht11Inst.read()
            
            if dht11Read.is_valid():
                textTweet = 'ゲンザイノ ニチジハ ' + current_time + ' キオン ' + str(dht11Read.temperature) + '℃ ' + 'シツド ' + str(dht11Read.humidity) + '% デス.'
                
                print(filePath)
                
                resCmd = subprocess.call(powerOnCmd.split())
                print(resCmd)
                time.sleep(3)
                
                if capt.putImage(filePath):
                    twitter.tweetImage(textTweet, filePath)
                else:
                    twitter.tweet(textTweet)
                
                print('success tweeted.')
                
                resCmd = subprocess.call(powerOffCmd.split())
                print(resCmd)
                time.sleep(1)

                errorCnt = 0
                loopRead = False
                
            else:
                print('dht11 error')
                
                if errorCnt > 49:
                    twitter.tweet('ヨミトリ エラー ガ 50カイ ヲ コエマシタ. カンシ ヲ チュウシ シマス.')
                    
                    print('error over 50. error tweeted.')
                    
                    loopRead = False
                    loopContinue = False
                
                elif errorCnt > 0 and errorCnt % 10 == 0:
                    print('error over 10. recreate dht11 instance.')
                    
                    errorCnt = errorCnt + 1
                    time.sleep(10)
                    
                    dht11Inst = dht11.DHT11(pin=4)
                else:
                    errorCnt = errorCnt + 1
                    time.sleep(3)

    time.sleep(sleepTime)

