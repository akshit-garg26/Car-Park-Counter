import cv2
import pickle
import cvzone
import numpy as np

# video feed
cap = cv2.VideoCapture('carPark.mp4')

width,height = 107,48

with open('CarParkPos','rb') as f:
    posList = pickle.load(f)

def checkParkingSpace(imgPro):
    spaceCounter = 0
    for pos in posList:
        x,y = pos
      

        imgCrop = imgPro[y:y+height,x:x+width]
        count = cv2.countNonZero(imgCrop)
        # cv2.imshow(str(x*y),imgCrop)
    

        if count<900:
            color=(0,255,0)
            thickness= 5
            spaceCounter +=1
        else:
            color=(0,0,255)
            thickness=2
        cv2.rectangle(img,(pos[0],pos[1]),(pos[0]+width,pos[1]+height),color,thickness)
        cvzone.putTextRect(img,str(count),(x,y+height-5),scale=1.5,thickness=2,offset=0,colorR=color)

    cvzone.putTextRect(img,f'Free:{spaceCounter}/{len(posList)}',(100,55),scale=3,thickness=5,offset=20,colorR=(0,210,0))

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES)== cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    success, img= cap.read()

    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    imgMedian = cv2.medianBlur(imgThreshold,5)
    kernel = np.ones((3,3),np.uint8)
    imgDilate = cv2.dilate(imgMedian,kernel,iterations=1)
    # cv2.imshow("gray_image",imgGray)
    # cv2.imshow("median image",imgMedian)
    checkParkingSpace(imgDilate)
    

    cv2.imshow("Image",img)
    cv2.waitKey(10)