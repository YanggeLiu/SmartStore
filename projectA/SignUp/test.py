#!/usr/bin/python3

import time
import face_detection


def progress_bar(num):
    t = '|/-\\'
    for i in range(0,num+1):
        s = ('='*i) + (' '*(num - i))
        print("[%s][%s][%.2f"%(t[i%4],s,(i/num*100)),"%]",end='\r')

        time.sleep(0.1)

    print()

progress_bar(40)

localtime = time.localtime(time.time())

print(localtime[3])

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


print(Hour)

face_detection.face_detection()
