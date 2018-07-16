# coding:utf-8

import cv2
import time

class ImageCapture:

    def __init__(self):
        print('initialized')

    def putImage(self, filePath):
        cap = cv2.VideoCapture(0)

        for i in xrange(30):
            ret, im = cap.read()

        ret, img = cap.read()

        if ret==True:
            cv2.imwrite(filePath, img)

        cap.release()
        
        return ret
