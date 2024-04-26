# we will see all the parking spaces and will see if it is vacant or not
# we have to do manual process one time
import cv2 
import pickle 
# to save all the positions of parking



width,height = 107,48

try:
    with open('CarParkPos','rb') as f:
        posList = pickle.load(f)
except:
    posList = []

# (720,1100,3) 

def mouseClick(events,x,y,flags,params):
    if events ==cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for index,pos in enumerate(posList):
            x1 = pos[0]
            y1 = pos[1]
            if x1<x<x1+width and y1<y<y1+height:
                posList.pop(index)
    with open('CarParkPos','wb') as f:
        pickle.dump(posList,f)

while True:
    # print(posList)
    img = cv2.imread('carParkImg.png')
    for pos in posList: 
        cv2.rectangle(img,(pos[0],pos[1]),(pos[0]+width,pos[1]+height),color=(0,0,0),thickness=2)

    cv2.imshow("Image",img)
    cv2.setMouseCallback("Image",mouseClick)
    cv2.waitKey(1)
# cv2.destroyAllWindows

