#!/usr/bin/python3

from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import argparse
import pickle
import sys
import os

sys.path.append("../Server")

import server


def train(number,name):
    if os.path.exists("../face_detector/out.pickle"):
        os.remove("../face_detector/out.pickle")

    if os.path.exists("../face_detector/le.pickle"):
        os.remove("../face_detector/le.pickle")
    
    print("[INFO] loading face embedding...")
    data = pickle.loads(open("../face_detector/embeddings.pickle",'rb').read())

    print('[INFO] encoding labels...')
    le = LabelEncoder()
    labels = le.fit_transform(data["name"])

    print("[INFO] training model...")
    recognizer = SVC(C=1.0,kernel="linear",probability=True)
    recognizer.fit(data["embedding"],labels)

    f = open("../face_detector/out.pickle",'wb')
    f.write(pickle.dumps(recognizer))
    f.close()

    f = open("../face_detector/le.pickle","wb")
    f.write(pickle.dumps(le))
    f.close()

    server.CreateAccount(number,name)



    print('==============================')

    print("All setting is done!")

    print("Welcome to Store!")


    print('==============================')