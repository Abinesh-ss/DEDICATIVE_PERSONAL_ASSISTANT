import cv2
from deepface import DeepFace
import time as t

cam=cv2.VideoCapture(0)

for i in range(10):
    ret,frame=cam.read()
    cv2.imwrite('opencv'+str(i)+'.png',frame)
del(cam)
t.sleep(3)
img=cv2.imread("C:\\Users\\abine\\Desktop\\py_projects\\opencv9.png")
result=DeepFace.analyze(img,actions=['emotion'])
value=result[0]["dominant_emotion"]
print(value)


