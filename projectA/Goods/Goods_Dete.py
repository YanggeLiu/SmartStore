#!/usr/bin/python3

import numpy as np
import argparse
import confirm_an_order
import time
import cv2
import sys
import os

sys.path.append('../Server')
import server

ap = argparse.ArgumentParser()
ap.add_argument('-c','--confidence',type=float,default=0.5,help='minimum probability to filter weak detections')
ap.add_argument('-t','--threshold',type=float,default=0.3,help="threshold when applying non-maxima suppression")

args = vars(ap.parse_args())

labelsPath = os.path.sep.join(['../Goods/YOLOv3','coco.names'])
LABELS = open(labelsPath).read().strip().split('\n')

np.random.seed(42)
COLORS = np.random.randint(0,255,size=(len(LABELS),3),dtype='uint8')

weightsPath = os.path.sep.join(['../Goods/YOLOv3','yolov3.weights'])
configPath = os.path.sep.join(['../Goods/YOLOv3','yolov3.cfg'])

print('[INFO] loading YOLO from disk...')
net = cv2.dnn.readNetFromDarknet(configPath,weightsPath)

cap = cv2.VideoCapture(0)
#startTime = time.time()

def Goods_dete(FINID):
    startTime = time.time()
    while True:
        ret,frame = cap.read()
        #cv2.imshow('Frame',frame)
        cv2.waitKey(1)
        if round(time.time() - startTime) == 5:
            print(round(time.time() - startTime))
            if os.path.exists('../Goods/Photo/Photo.jpg'):
                os.remove('../Goods/Photo/Photo.jpg')
                print('remove')
            cv2.imwrite('../Goods/Photo/Photo.jpg',frame)
            print('Get the Goods\n\nLoading...')
            image = cv2.imread('../Goods/Photo/Photo.jpg')
            (H,W) = image.shape[:2]

            ln = net.getLayerNames()
            ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

            blob = cv2.dnn.blobFromImage(image, 1/255.0,(416,416),swapRB=True,crop=False)
            net.setInput(blob)
            start = time.time()
            layerOutputs = net.forward(ln)
            end = time.time()

            print('[INFO] YOLO took {:.6f} seconds'.format(end - start))

            boxes = []
            confidences = []
            classIDs = []

            for output in layerOutputs:
                for detection in output:
                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]

                    if confidence > args['confidence']:
                        box = detection[0:4] * np.array([W,H,W,H])
                        (centerx,centerY,width,height) = box.astype('int')

                        x = int(centerx - (width / 2))
                        y = int(centerY - (height / 2))

                        boxes.append([x,y,int(width),int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)
            
            idxs = cv2.dnn.NMSBoxes(boxes,confidences,args['confidence'],args['threshold'])

            if len(idxs) > 0:
                Goods = []
                for i in idxs.flatten():
                    (x,y) = (boxes[i][0],boxes[i][1])
                    (w,h) = (boxes[i][2],boxes[i][3])

                    text = "{}:{:4f}".format(LABELS[classIDs[i]],confidences[i])
                    Goods.append(LABELS[classIDs[i]])
                    print(text)
                    startTime = time.time()
                if server.Check_Face(FINID) == '0':
                    print('Uploading bill')
                    print('=======================')
                    print(Goods)
                    print('=======================')
                    key = input('The bill is right?(Y or N)\n')
                    if key == 'y':
                        print('Okay,Please wait...')
                        confirm_an_order.confirm(FINID,Goods)
                        break
                    elif key == 'n':
                        print('Okay,It may will be check again,please wait...')
                        startTime = time.time()
                        continue

    cap.release()
    cv2.destroyAllWindows()