#!/usr/bin/python3

from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import pickle
import time
import sys
import cv2
import os

sys.path.append("../Server")

import server

ap = argparse.ArgumentParser()
#ap.add_argument('-d',"--detector",required=True,help="path to OpenCV's deep learning face detector")
#ap.add_argument('-m','--embedding-model',required=True,help="path to OpenCV's deep learning face embeddins model")
#ap.add_argument('-r','--recognizer',required=True,help="path to trained to recognize faces")
#ap.add_argument('-l',"--le",required=True,help="path to label encoder")
ap.add_argument('-c','--confidence',type=float,default=0.5,help="minimum probability to filter weak detections")

args = vars(ap.parse_args())

print('[INFO] loading face detector...')
protoPath = os.path.sep.join(['../face_detector','deploy.prototxt'])
modelPath = os.path.sep.join(['../face_detector','res10_300x300_ssd_iter_140000.caffemodel'])

detector = cv2.dnn.readNetFromCaffe(protoPath,modelPath)

print("[INFO] loading face recognizer...")
embedder = cv2.dnn.readNetFromTorch('../face_detector/nn4.small2.v1.t7')

recognizer = pickle.loads(open('../face_detector/out.pickle','rb').read())
le = pickle.loads(open('../face_detector/le.pickle',"rb").read())

vs = VideoStream(src=0).start()
time.sleep(2.0)

fps = FPS().start()

while True:
    frame = vs.read()
    frame = imutils.resize(frame,width=600)
    (h,w) = frame.shape[:2]

    imageBlob = cv2.dnn.blobFromImage(cv2.resize(frame,(300,300)),1.0,(300,300),(140.0,177.0,123.0),swapRB=False,crop=False)

    detector.setInput(imageBlob)
    detections = detector.forward()

    for i in range(0,detections.shape[2]):
        confidence = detections[0,0,i,2]

        if confidence > args['confidence']:
            box = detections[0,0,i,3:7] * np.array([w,h,w,h])
            (startX,startY,endX,endY) = box.astype('int')

            face = frame[startY:endY,startX:endX]
            (fH,fW) = face.shape[:2]

            if fW <20 or fH <20:
                continue

            faceBlob = cv2.dnn.blobFromImage(face,1.0/255,(96,96),(0,0,0),swapRB=True,crop=False)
            embedder.setInput(faceBlob)
            vec = embedder.forward()

            preds = recognizer.predict_proba(vec)[0]
            j = np.argmax(preds)
            proba = preds[j]
            name = le.classes_[j]

            text = "{}:{:.2f}%".format(name,proba*100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(frame,(startX,startY),(endX,endY),(0,0,255),2)
            cv2.putText(frame,text,(startX,y),cv2.FONT_HERSHEY_COMPLEX,0.45,(0,0,255),2)
            if name and name != 'unknown':
                server.Change_Face(str(name))
                print('Please wait...')

    
    fps.update()
    cv2.imshow("Frame",frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

fps.stop()
print('[INFO] elasped time: {:.2f}'.format(fps.elapsed()))
print('[INFO] approx FPS: {:.2f}'.format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()


