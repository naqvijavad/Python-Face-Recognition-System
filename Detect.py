# Importing Required Packages
import cv2
import projectmodules as pm
import csv

modeexcel=r'.\Datafiles\modeofdetect.xlsx'
modecsv=r'.\Datafiles\modeofdetect.csv'
train_file = r'.\Recognizer\Trained_data.yml'
# Creating an empty list of labels and empployee
labels = []
employee = []
ret_val=""
pm.from_excel_to_csv(modeexcel,modecsv)
with open(modecsv,'r') as f:
    data=csv.reader(f)
    lines=list(data)
    for line in lines:
        ret_val=line[1]
        break
pm.update_excel(modecsv,modeexcel)

# Starting Video Capture
cap = cv2.VideoCapture(0)
excelfile = r'.\Datafiles\AttendanceReport.xlsx'
csvfile = r'.\Datafiles\AttendanceReport.csv'

# Converting Excel to csv
pm.from_excel_to_csv(excelfile, csvfile)

# Getting data from the csv file
names = pm.get_employee_data(csvfile)

# Creating recognizer and then training the recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(train_file)

# Defining the face and eye cascade classifier
face_xml = r'.\res\haarcascade_frontalface_default.xml'
eye_xml = r'.\res\haarcascade_eye_tree_eyeglasses.xml'
haar_cascade_classifier = cv2.CascadeClassifier(face_xml)
eye_classifier = cv2.CascadeClassifier(eye_xml)

# Creating an empty list of the employee which blinks
blink_list = []
eye_flg = True
show_count = True
blinks = 0

# Looping through the frames captured
while cap.isOpened():
    ret, img = cap.read()
    contstimg = cv2.convertScaleAbs(img, alpha=1.5, beta=0.0)  # Adding contrast to the image
    biltstimg = cv2.bilateralFilter(contstimg, 5, 75, 75)  # Applying Bilateral filter to the image
    img = cv2.addWeighted(biltstimg, 0.5, img, 0.5, 0.0)  # Blending the image

    if ret_val=="True":  # Turbo Mode
        img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)  # Denoiseing the image

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # converting img to gray color image
    # detecting face co-ordinates using the face cascade classifier
    faces_detected = haar_cascade_classifier.detectMultiScale(gray_img, scaleFactor=1.32, minNeighbors=5)
    for x, y, w, h in faces_detected:  # looping through each face coordinates
        face = (x, y, w, h)
        eye_flg = False
        pm.drawrect(face, img)  # Applying rectangle around the face
        label, confidence = recognizer.predict(gray_img[y:y + h, x:x + w])  # Predicting the face
        predictedname = names[label]  # defining the predicted name
        roi_gray_eyes = gray_img[y:y + h, x:x + w]  # region of intereset for eye in gray color image
        roi_color_eyes = img[y:y + h, x:x + w]  # region of interest for eye in normal color image
        # detecting eyes co-ordinates using the eye cascade classifier
        eyes = eye_classifier.detectMultiScale(roi_gray_eyes, scaleFactor=1.32, minNeighbors=5)
        for ex, ey, ew, eh in eyes:
            eye = (ex, ey, ew, eh)
            eye_flg = True
            pm.drawrect(eye, roi_color_eyes)  # Applying rectangle around the eyes
        if eye_flg:
            show_count = True

        if show_count and not eye_flg:
            show_count = False
            blink_list.append(label)  # Appending the employee id who blinks

        if confidence < 100:
            pm.putnames(x, y, predictedname, img)  # putting text above the rectangle
            labels.append(label)  # appending label in labels list
            employee.append(names[label])  # appending employee in employee list
            justlabels = set(labels)  # creating a set of labels
            totalemployee = set(employee)  # creating a set of total employee
            blinks = set(blink_list)  # creating a set of blink list
            for i in justlabels:
                if labels.count(i) >= 5:  # if labels of employee is more than 5
                    for j in blinks:
                        if blink_list.count(j) >= 2:  # if blink of employee is more than 2 then marking present
                            pm.mark_present(i)  # marking present of employee

    cv2.imshow('FaceRecognition', img)  # showing the video capture frames
    if cv2.waitKey(1) == ord('s'):  # if user press the s key
        pm.update_excel(csvfile, excelfile)  # updating the excel from csvfile to excelfile
        break

cap.release()  # release the cap variable
cv2.destroyAllWindows()  # destroying all windows

