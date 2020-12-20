#!/usr/bin/python3
#--coding:utf8--

from imutils.video import VideoStream
import extract_embeddings
import imutils
import argparse
import time
import cv2
import os

def face_detection(number,name):
    print('==============================')

    print('Step Two')

    print('Create face detection')

    print('==============================')

    path = '../Dataset/'+name

    os.mkdir(path)

    detector = cv2.CascadeClassifier('../face_detector/haarcascade_frontalface_default.xml')

    print('[INFO] starting video stream...')
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    total = 0

    while True:
        frame = vs.read()
        orig = frame.copy()
        frame = imutils.resize(frame,width=400)

        rects = detector.detectMultiScale(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY),scaleFactor=1.1,minNeighbors=5,minSize=(30,30))

        for (x,y,w,h) in rects:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        cv2.imshow('face detection',frame)
        cv2.waitKey(1)
        p = os.path.sep.join([path,"{}.png".format(str(total).zfill(5))])
        cv2.imwrite(p,orig)
        total += 1
        time.sleep(1)
        if total == 12:
            break

    print('[INFO] {} face images stored'.format(total))
    print('[INFO] cleaning up...')
    cv2.destroyAllWindows()
    vs.stop()
    extract_embeddings.extract(number,name)