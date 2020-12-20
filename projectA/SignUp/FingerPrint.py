#!/usr/bin/python3
#--coding:utf8--

import serial
import time
import Dataset

print('==============================')

print('Welcome to my world')

print('Writen by Yangge')

print('==============================')

#Create new fingerprint
print('Step One')

print('Create new fingerprint')

print('==============================')

ACK_SUCCESS = 0x00
ACK_FAIL = 0x01
ACK_FULL = 0x04
ACK_FIN_OPD = 0x07
ACK_TIMEOUT = 0x08

ser = serial.Serial('/dev/ttyUSB0',19200,timeout=0.5)

CheckAccountMum = bytes([0xf5,0x09,0x00,0x00,0x00,0x00,0x09,0xf5])

send = ser.write(CheckAccountMum)

backdata = ser.read(send)

Len = backdata[3]

print('Account number is :%d'%int(Len))

name = input("Hello,What's your name?\n")

localtime = time.localtime(time.time())

morning = 'Good morning'
afternoon = 'Good afternoon'
evening = 'Good evening'
Hour = ''

if 1 <= localtime[3] <= 11:
    Hour = morning
elif 12 <= localtime[3] <= 17:
    Hour = afternoon
elif 18 <= localtime[3] <= 24:
    Hour = evening


print(Hour+', '+name)

ask = input('Create a new account?(Y or N):')

if ord(ask) == ord('y'):
    a = 0x1
    b = 0x00
    number = int(Len) + 1
    c = 0x01
    d = 0x00
    CHK = a ^ b ^ number ^ c ^ d
    create = bytes([0xf5,a,b,number,c,d,CHK,0xf5])
    send = ser.write(create)
    print('Please put your finger on the modules')
    while True:
        backdata = ser.read(send)
        if len(backdata) == send:
            print('get')
            break
    if backdata[4] == ACK_SUCCESS:
        a = 0x2
        CHK = a ^ b ^ number ^ c ^ d
        create = bytes([0xf5,a,b,number,c,d,CHK,0xf5])
        send = ser.write(create)
        print('Please put your finger on the modules again')
        while True:
            backdata = ser.read(send)
            if len(backdata) == send:
                print('get')
                break
        if backdata[4] == ACK_SUCCESS:
            a = 0x3
            CHK = a ^ b ^ number ^ c ^ d
            create = bytes([0xf5,a,b,number,c,d,CHK,0xf5])
            send = ser.write(create)
            print('It would be done')
            while True:
                backdata = ser.read(send)
                if len(backdata) == send:
                    print('get')
                    break
            if backdata[4] == ACK_SUCCESS:
                print('Everything is DONE')
                Dataset.face_detection(number,name)
            elif backdata[4] == ACK_FAIL:
                print('Error')
            elif backdata[4] == ACK_FIN_OPD:
                print('The finger is OPD')
            elif  backdata[4] == ACK_TIMEOUT:
                print('Time is out')
        elif backdata[4] == ACK_FAIL:
            print('Error')
        elif  backdata[4] == ACK_FIN_OPD:
            print('The finger is OPD')
        elif backdata[4] == ACK_TIMEOUT:
            print('Time is out')
    elif backdata[4] == ACK_FAIL:
        print('Error')
    elif backdata[4] == ACK_FIN_OPD:
        print("The finger is OPD")
    elif backdata[4] == ACK_FULL:
        print('The modules is full')
    elif backdata[4] == ACK_TIMEOUT:
        print('Time is out')

elif ord(ask) == ord('n'):
    print('Okay...')