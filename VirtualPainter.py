import cv2
import numpy as np
import time
import HandTrackingModule as htm

Img=cv2.imread('1.png')
cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

imgCanvas=np.zeros((720,1280,3),np.uint8)

drawColor=(255,0,255)
xp,yp=0,0
brushthickness=15

detector=htm.handDetector()


while True:
    success,img=cap.read()
    img=cv2.flip(img,1)

    img[0:125,0:1280]=Img

    img=detector.findHands(img)
    lmList=detector.findPosition(img)
    if len(lmList)!=0:

        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]

        fingers=detector.fingersUp()

        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            print("selection")
            if y1<125:
                if 250<x1<450:
                    drawColor=(255,0,255)
                elif 550<x1<750:
                    drawColor=(255,0,0)
                elif 800<x1<950:
                    drawColor=(0,255,0)
                elif 1050<x1<1280:
                    drawColor=(0,0,0)

            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 - 25), drawColor, cv2.FILLED)

        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
            print("drawing")
            if xp==0 and yp==0:
                xp,yp=x1,y1

            if drawColor==(0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor,50)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, 50)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushthickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushthickness)
            xp,yp=x1,y1

    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _,imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,imgInv)
    img=cv2.bitwise_or(img,imgCanvas)



    cv2.imshow('Image',img)
    #cv2.imshow('Imageq', imgCanvas)
    cv2.waitKey(1)