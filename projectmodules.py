#importing Required Packages
import csv
import cv2
import pandas as pd
import numpy as np
import os


def facedetection(img):
    """This Function takes image as argument and apply contrast, bilateral filter and denoise the image
     and return the x,y,w,h co-ordinates of faces and also gray color image"""
    face_xml=r'.\res\haarcascade_frontalface_default.xml'
    haar_cascade_classifier=cv2.CascadeClassifier(face_xml)
    contstimg = cv2.convertScaleAbs(img, alpha=1.5, beta=0.0)
    biltstimg = cv2.bilateralFilter(contstimg, 5, 75, 75)
    img = cv2.addWeighted(biltstimg, 0.5, img, 0.5, 0.0)
    img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
    gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=haar_cascade_classifier.detectMultiScale(gray_img,scaleFactor=1.32,minNeighbors=5)
    return faces,gray_img


def training_data(directory):
    """This Funcation takes directory path as argument and makes list of faces co-ordinates and its id
        of image which are available in the directory and returns the list of face-coordinates and list of faceid
        which can be used to train the classifier"""
    faces=[]
    faceid=[]

    for root,subdirname,filenames in os.walk(directory):
        for filename in filenames:
            id=os.path.basename(root)
            img_path=os.path.join(root,filename)
            img=cv2.imread(img_path)
            face,gray_img=facedetection(img)
            if len(face)!=1:
                continue
            (x,y,w,h)=face[0]
            roi_gray_img=gray_img[y:y+h,x:x+w]
            roi_gray_img=cv2.resize(roi_gray_img,(100,100))
            faceid.append(int(id))
            faces.append(roi_gray_img)

    return faces,faceid


def train_classifier(faces,faceid):
    """This function takes list of face co-ordinate along with list of ids and trains the classifier which can be
        used to predict the face and return the recognizer"""
    recognizer=cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces,np.array(faceid))

    return recognizer


def drawrect(face,img):
    """This Function takes face co-ordinates, image and draw a rectangle around the face in image and
    then return the image"""
    (x,y,w,h)=face
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)

    return img


def putnames(x,y,text,img):
    """This function takes x-y co-ordinates, text and image and put text above the rectangle and
    return the image"""
    cv2.putText(img,text,(x,y),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)

    return img


def from_excel_to_csv(excelfile,csvfile):
    """This function take the excel and csv file name as argument and then convert excel file to csvfile"""
    df=pd.read_excel(excelfile)
    with open(csvfile,'w') as f:
        f.truncate()
    df.to_csv(csvfile)


def get_employee_data(csvfile):
    """This function take the csvfile name as argument and returns a dictionary of data of the csvfile"""
    names={}
    with open(csvfile,'r') as f:
        data=csv.reader(f)
        next(data)
        lines=list(data)
        for line in lines:
            names[int(line[1])]=line[2]

    return names


def mark_present(id):
    """This function takes id of the predicted face and marks present on the csv file of attendance report"""
    csv_areport=r'.\Datafiles\AttendanceReport.csv'
    with open(csv_areport,'r') as f:
        data=csv.reader(f)
        lines=list(data)
        for line in lines:
            if line[1]==str(id):
                line[-1]='P'
                with open(csv_areport,'w') as g:
                    writer=csv.writer(g,lineterminator='\n')
                    writer.writerows(lines)
                    break


def update_excel(csvfile,excelfile):
    """This function takes csv and excel file name as argument and remove the first column of csvfile which are index
        and then convert the csvfile to excelfile"""
    with open(csvfile) as f:
        data=csv.reader(f)
        lines=list(data)
        for line in lines:
            line.pop(0)
        with open(csvfile,'w') as g:
            writer=csv.writer(g,lineterminator='\n')
            writer.writerows(lines)

    df=pd.read_csv(csvfile)
    df.to_excel(excelfile,index=False)


