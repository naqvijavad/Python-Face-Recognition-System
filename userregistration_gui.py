# Importing Required packages
import tkinter
from tkinter import *
from tkinter import messagebox
import re
import csv
import os
import pandas as pd
from PIL import ImageTk
import projectmodules as pm

window = Tk()  # creating a window name window


def go_to_maingui():
    """This function redirect ot main gui and destroy current window"""
    window.destroy()
    os.system('maingui.py')


def go_to_trainuser():
    """This function validates the input name and id and then registers the user in employee data and attendance
        report file"""
    ename = name_inp.get()  # storing name from entry
    eid = id_inp.get()  # storing id from entry
    edept=dept_inp.get() # storing departemnt from entry

    res_name = bool(re.search(r'\d', ename))  # regular expression search for is there is any digit in name
    res_id = eid.isdigit()  # returns True if all the characters are digits
    res_dept = bool(re.search(r'\d', edept))  # regular expression search for is there is any digit in name
    # returns True if all the characters in a string are not whitespaces and name is also not empty
    res_name_empty=bool(ename and not ename.isspace())
    res_dept_empty=bool(edept and not edept.isspace())
    res_eid_empty=bool(eid and not eid.isspace())

    if res_name_empty==False or res_eid_empty==False or res_dept_empty==False:  # if name or id is empty
        tkinter.messagebox.showerror(title="Error", message="Cannot leave a field blank")  # display error
    elif res_name==True or res_id==False or res_dept==True:  # if name contains a digit or id contains a character
        tkinter.messagebox.showerror(title="Error", message="Please enter correct data")  # display error
    else:
        excelfile_empdata = r'.\Datafiles\EmployeeData.xlsx'
        excelfile_areport = r'.\Datafiles\AttendanceReport.xlsx'
        csvfile_empdata = r'.\Datafiles\EmployeeData.csv'
        csvfile_areport = r'.\Datafiles\AttendanceReport.csv'

        pm.from_excel_to_csv(excelfile_empdata,csvfile_empdata)  # converting from excel to csv
        with open(csvfile_empdata,'r') as f:   # opening file in read mode
            flag=0
            data=csv.reader(f)
            lines=list(data)

            for line in lines:
                if line[1]==eid:
                    tkinter.messagebox.showerror(title="Error",message="User already Registered")  # display error
                    flag=1
                    break

            if flag==0:
                edata = [eid,ename,edept]

                with open(csvfile_empdata) as f:  # opening file in read mode
                    data = csv.reader(f)
                    lines = list(data)
                    for line in lines:
                        line.pop(0)
                    with open(csvfile_empdata,'w') as g:   # opening file in write mode
                        writer=csv.writer(g,lineterminator='\n')
                        writer.writerows(lines)

                with open(csvfile_empdata,'a+') as g:  # opening  file in append mode
                    writer=csv.writer(g,lineterminator='\n')
                    writer.writerow(edata)
                df=pd.read_csv(csvfile_empdata)  # reading csv file
                df.to_excel(excelfile_empdata,index=False)  # converting csv to excel

                pm.from_excel_to_csv(excelfile_areport,csvfile_areport)  # converting from excel to csv
                with open(csvfile_areport) as f:  # opening file in read mode
                    data = csv.reader(f)
                    lines = list(data)
                    for line in lines:
                        line.pop(0)
                    with open(csvfile_areport,'w') as g:  # opening file in write mode
                        writer=csv.writer(g,lineterminator='\n')
                        writer.writerows(lines)

                with open(csvfile_areport,'a+') as g:  # opening file in append mode
                    writer=csv.writer(g,lineterminator='\n')
                    writer.writerow(edata)
                df=pd.read_csv(csvfile_areport)
                df.to_excel(excelfile_areport,index=False)  # converting from csv to excel
                os.system('Trainuser.py')  # redirecting to trainuser script
                result=Label(window.frame,text="User Registered and Trained Successfully",bg="white"
                             ,fg="blue",font=("Arial",12,"bold"))
                result.place(x=10,y=250,width=400)


window.geometry("1200x700+150+50")  # creating window with 1200px width 700px height and 150 from x axis and 50 from y
window.title("USER REGISTRATION FORM")  # giving title to window
window.resizable(width=False,height=False)  # setting width and height non-resizeable
bkimage=ImageTk.PhotoImage(file="./Images/background1.jpg")
imglbl=Label(window,image=bkimage)  # setting image as label in background
imglbl.pack()  # packing the image label

window.frame=Frame(window,background="black")  # creating a frame in window with black background
window.frame.place(x=315,y=150,width=600,height=400)  # assigning the frame at given co-ordinates


# creating label
name_label=Label(window.frame,text="Employee Name",bg="white",fg="blue",font=("Arial",12,"bold"))
id_label=Label(window.frame,text="Employee Id",bg="white",fg="blue",font=("Arial",12,"bold"))
dept_label=Label(window.frame,text="Employee Department",bg="white",fg="blue",font=("Arial",12,"bold"))

# positioning the label
name_label.place(x=10,y=10,width=200)
id_label.place(x=10,y=80,width=200)
dept_label.place(x=10,y=150,width=200)

# crating entry to get input from user
name_inp=Entry(window.frame,bg="white",fg="blue",font=("Arial",12,"bold"))
id_inp=Entry(window.frame,bg="white",fg="blue",font=("Arial",12,"bold"))
dept_inp=Entry(window.frame,bg="white",fg="blue",font=("Arial",12,"bold"))

# positioning the entry
name_inp.place(x=240,y=10,width=200)
id_inp.place(x=240,y=80,width=200)
dept_inp.place(x=240,y=150,width=200)

# creating buttons
back_btn=Button(window.frame,text="BACK",command=go_to_maingui,activebackground="blue"
                           ,activeforeground="white",fg="blue",bg="white",font=("Arial",12,"bold"))
register_btn=Button(window.frame,text="Register",command=go_to_trainuser,activebackground="blue"
                           ,activeforeground="white",fg="blue",bg="white",font=("Arial",12,"bold"))

# positioning button
back_btn.place(x=10,y=200,width=200)
register_btn.place(x=240,y=200,width=200)

# looping through window
window.mainloop()

