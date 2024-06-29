import cv2
import time
import handtrackingmodule as htm
import numpy as np
import os
import pyttsx3

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

speak("please wait for few seconds...")

overlayList=[]

brushThickness = 20
eraserThickness = 60
drawColor=(255,0,255)

xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

overlayList = []


folderPath ="F://ai//AI-Virtual-Paint-main-20240416T061515Z-001//AI-Virtual-Paint-main//AI-Virtual-Paint-main//Header"


if os.path.exists(folderPath):

    myList = os.listdir(folderPath)
    

    for imPath in myList:

        image = cv2.imread(os.path.join(folderPath, imPath))
        overlayList.append(image)

    if overlayList:

        header = overlayList[0]
        

        cap = cv2.VideoCapture(0)
        
       
        cap.set(3, 3840)  # width
        cap.set(4, 2160)   # height
    else:
        print("No images found in the directory.")
else:
    print("The specified directory does not exist:", folderPath)

detector = htm.handDetector(detectionCon=0.50,maxHands=1)

speak("draw now")
while True:


    success, img = cap.read()
    
    if not success:
        print("Failed to capture video feed.")
        break
    
    img=cv2.flip(img,1)
    
     
    img = detector.findHands(img)
    lmList,bbox = detector.findPosition(img, draw=False)
    
    if len(lmList)!=0:
        
        x1, y1 = lmList[8][1],lmList[8][2]
        x2, y2 = lmList[12][1],lmList[12][2]
        
        
        fingers = detector.fingersUp()
       

        
        if fingers[1] and fingers[2]:
            xp,yp=0,0
            
            if y1 < 125:
                if 250 < x1 < 450:#if i m clicking at red brush
                    header = overlayList[0]
                    drawColor = (0, 0, 255)
                elif 550 < x1 < 750:#if i m clicking at cany brush
                    header = overlayList[1]
                    drawColor = (225, 225, 0)
                elif 800 < x1 < 950:#if i m clicking at green brush
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 1050 < x1 < 1200:#if i m clicking at eraser
                    header = overlayList[3]
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)


        
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
           
            if xp == 0 and yp == 0:
                xp, yp = x1, y1 
            
            
            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp,yp=x1,y1 
           
           
    

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    

    img = cv2.bitwise_or(img,imgCanvas)


    img[0:125,0:1280]=header

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    


    