# importing the cv2 library for working on images
import cv2
# importing the numpy library for working on the multidimensional arrays
import numpy as np
#importing pandas to work on dataframe
import pandas as pd

#importing the dataset of students 
df=pd.read_csv('data.csv')
df.set_index('ID',inplace=True)
#using the haarcascade frontalface as a cascade classifier
faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#capturing video using the webcam
cam=cv2.VideoCapture(0)
#using the LBPH algorithm for face recognition
rec=cv2.face.LBPHFaceRecognizer_create()
#reading the trained file
rec.read('trainer.yml')
#setting id to zero
id=0

#setting the video width
cam.set(3, 640) 
# setting video height
cam.set(4, 480) 
#font=cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX_SMALL,1,1,0,1)
#deciding the font for the text in video
font = cv2.FONT_HERSHEY_SIMPLEX
while(True):
    #reading image frame by frame
    ret,img=cam.read()
    #converting the image to grayscale
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #detecting the face
    faces=faceDetect.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        #creating a rectangle for the detected face
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        #getting the id and the confidence
        id,confidence=rec.predict(gray[y:y+h,x:x+w])
        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 100):
            id = id
            confidence = "  {0}%".format(round(100 - confidence))
            #updating the attendance column
            df.Attendance[df.index==id]="present"
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        #displaying the image along with the id and confidence
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
    #saving the csv file
    df.to_csv('data.csv')
    cv2.imshow("Face",img)
    #killing the loop
    if(cv2.waitKey(1)==ord('q')):
        break
cam.release()
cv2.destroyAllWindows()