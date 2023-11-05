# Importing required packages
import csv
import os
import cv2
import projectmodules as pm

cap=cv2.VideoCapture(0)  # starting video capture from camera
face_xml=r'.\res\haarcascade_frontalface_default.xml'
haar_cascade = cv2.CascadeClassifier(face_xml)  # defining the face cascade classifier
excelfile=r'.\Datafiles\EmployeeData.xlsx'
csvfile=r'.\Datafiles\EmployeeData.csv'
pm.from_excel_to_csv(excelfile,csvfile)  # converting excel to csv
names=pm.get_employee_data(csvfile)  # getiing employee data in names dictionary
ask=len(names.keys())
""" reading the csvfile and if the no.of employee is equal to the ask variable them assigning to id which is uesd to
    directory for captured iamges of employee"""
with open(csvfile,'r') as f:
    data=csv.reader(f)
    lines=list(data)
    k=0
    for line in lines:
        k=k+1
        if ask+1==k:
            id=line[1]


directory=f".\Dataset\{id}"
os.mkdir(directory)  # creating directory for storing images of user
# maindirectory=r'....'
cntr=1
os.chdir(directory)  # changing directory for storing in that directory
i=1
while(cap.isOpened()):  # looping through captured frames
    i=i+1
    res, img = cap.read()
    # detecting face co-ordinates using the eye cascade classifier
    faces=haar_cascade.detectMultiScale(img,scaleFactor=1.32,minNeighbors=5)
    if len(faces)!=1:
        continue
    elif i%6==0:
        contstimg = cv2.convertScaleAbs(img, alpha=1.5, beta=0.0)  # adding contrast to image
        biltstimg = cv2.bilateralFilter(contstimg, 5, 75, 75)  # adding bilateral filter
        img = cv2.addWeighted(biltstimg, 0.5, img, 0.5, 0.0)  # blending the image
        fname = f"frame{cntr}.png"  # defining file name
        cv2.imwrite(fname,img)  # saving the image with defined filename
        cntr=cntr+1
        cv2.imshow('user image',img)  # showing the frame window
        if cv2.waitKey(1)==ord('q'):  # if user press q to exit
            break

# changing to main directory
os.chdir("..")
os.chdir("..")
cap.release()   # release the cap variable
cv2.destroyAllWindows()    # destroying all the windows
os.system('TrainingData.py')  # redirecting to Trainingdata script for data train

