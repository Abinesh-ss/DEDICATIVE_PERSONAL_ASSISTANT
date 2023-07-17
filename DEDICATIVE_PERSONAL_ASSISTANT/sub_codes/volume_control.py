import cv2 
import mediapipe as mp
from math import hypot
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume
import numpy as np

cap=cv2.VideoCapture(0)

mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils

devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))
volbar=400
volper=0

volmax,volmin=volume.GetVolumeRange()[:2]


while True:
    ret,img=cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)

    lmlist=[]
    if results.multi_hand_landmarks:
        for handlandmark in results.multi_hand_landmarks:
            for id,lm in enumerate(handlandmark.landmark):
                h,w,_=img.shape
                cx,cy=int (lm.x*w),int(lm.y*h)
                lmlist.append([id,cx,cy])
            mpDraw.draw_landmarks(img,handlandmark,mpHands.HAND_CONNECTIONS)
    if lmlist !=[]:
        x1,y1=lmlist[4][1],lmlist[4][2]
        x2,y2=lmlist[8][1],lmlist[8][2]

        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(0,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),3)

        length=hypot(x2-x1,y2-y1)

        vol=np.interp(length,[30,350],[volmax,volmin])
        volbar=np.interp(length,[30,350],[400,150])
        volper=np.interp(length,[30,350],[0,100])

        print(vol,int(length))
        volume.SetMasterVolumeLevel(vol,None)

        cv2.rectangle(img,(50,150),(85,400),(0,0,255),5)
        cv2.rectangle(img,(50,int(volbar)),(85,400),(0,0,255),cv2.FILLED)
        cv2.putText(img,f"{int(volper)}%",(10,40),cv2.FONT_ITALIC,1,(6,7,34),3)

    cv2.imshow("frame",img)
    if cv2. waitKey(1)==27:
        break
cv2.destroyAllWindows
cap.release()