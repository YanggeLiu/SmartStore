#!/usr/bin/python3

from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import pickle
import serial
import time
import cv2
import sys
import os

sys.path.append("../Server")
sys.path.append('../Goods')

import Goods_Dete
import server

print('==============================')

print("Welcome to Store")

print("Please look at the Camera, which can recognize you")

print('==============================')

ACK_SUCCESS = 0x00
ACK_FAIL = 0x01
ACK_FULL = 0x04
ACK_FIN_OPD = 0x07
ACK_TIMEOUT = 0x08
ACK_NOUSER = 0x05

ser = serial.Serial('/dev/ttyUSB0',19200,timeout=0.5)

CheckAccountMum = bytes([0xf5,0x0c,0x0,0x0,0x0,0x0,(0x0c^0x0^0x0^0x0^0x0),0xf5])

ser = serial.Serial('/dev/ttyUSB0',19200,timeout=0.5)

send = ser.write(CheckAccountMum)
while True:
    backdata = ser.read(send)
    if len(backdata) == send:
        if backdata[4] == ACK_NOUSER:
            print('No such USER')
            break
        print(backdata)
        print('Hello, '+str(backdata[3]))
        server.Login_FIN(str(backdata[3]))
        print("Waiting...")
        #time.sleep(3)
        if server.Check_status(str(backdata[3])) == '1':
            print("Let's bug something!")
            Goods_Dete.Goods_dete(str(backdata[3]))


        break