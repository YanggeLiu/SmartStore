#!/usr/bin/python3

import serial
import sys

sys.path.append('../Server')
import Goods_bill
import server

ACK_SUCCESS = 0x00
ACK_FAIL = 0x01
ACK_FULL = 0x04
ACK_FIN_OPD = 0x07
ACK_TIMEOUT = 0x08
ACK_NOUSER = 0x05

ser = serial.Serial('/dev/ttyUSB0',19200,timeout=0.5)

CheckAccountID = bytes([0xf5,0x0c,0x0,0x0,0x0,0x0,(0x0c^0x0^0x0^0x0^0x0),0xf5])

def confirm(FINID,Item):
    print('======================')
    print('Please put your finger to confirm')
    print(Item)
    send = ser.write(CheckAccountID)
    while True:
        backdata = ser.read(send)
        if len(backdata) == send:
            if backdata[4] == ACK_NOUSER:
                print('No such USER')
                break
            if str(backdata[3]) == FINID:
                Price = Goods_bill.Check_Price(Item)
                Balance = server.Check_Balance(str(backdata[3]))
                if Price > Balance:
                    print('Your Balance is not enough')
                    break
                server.Change_balance(FINID,(Balance - Price))
                server.Change_FIN(str(backdata[3]))
                server.Change_status(str(backdata[3]))
                if server.Check_status(str(backdata[3])) == '0':
                    print('goodbye!') 

