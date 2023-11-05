# Importing required packages
from tkinter import *
import os
from PIL import ImageTk
import tkinter.messagebox
import csv
import tkinter
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import projectmodules
import pandas
import xlrd


def call_registration_gui():
    """This function call user registration script and destroy current window"""
    window.destroy()
    os.system('userregistration_gui.py')


def call_attendance_gui():
    """This function call take attendance script and destroy current window"""
    train_file = r'.\Recognizer\Trained_data.yml'
    #  Checking if trained data file is created or not otherwise it will create by calling the Trainingdata script
    if not os.path.isfile(train_file):
        tkinter.messagebox.showerror(title="Error", message="First Train user and then check for attendance")
    else:
        window.destroy()
        os.system('takeattendance_gui.py')


def call_view_attendance():
    """This function view the attendance report file"""
    pathfor_attendance=r'.\Datafiles\AttendanceReport.xlsx'
    os.startfile(pathfor_attendance)


def call_deleteuser_gui():
    """This function call delete user script and destroy current window"""
    window.destroy()
    os.system('deleteuser.py')


window=Tk()  # creating a window name window
window.geometry("1200x700+150+50")  # creating window with 1200px width 700px height and 150 from x axis and 50 from y
window.title("FACE RECOGNITION SYSTEM")  # giving title to window
window.resizable(width=False,height=False)  # setting width and height non-resizeable

bkimage=ImageTk.PhotoImage(file="./Images/background1.jpg")
imglbl=Label(window,image=bkimage)  # setting image as label in background
imglbl.pack()  # packing the image label

window.frame=Frame(window,background="black")  # creating a frame in window with black background
window.frame.place(x=315,y=150,width=600,height=400)  # assigning the frame at given co-ordinates

# creating buttons
user_registration=Button(window.frame,text="User Registration",command=call_registration_gui,activebackground="blue"
                         ,activeforeground="white",fg="blue",bg="white",font=("Arial",15,"bold"))
Take_attendance=Button(window.frame,text="Take Attendance",command=call_attendance_gui,activebackground="blue"
                       ,activeforeground="white",fg="blue",bg="white",font=("Arial",15,"bold"))
delete_user=Button(window.frame,text="Delete User",command=call_deleteuser_gui,activebackground="blue"
                   ,activeforeground="white",fg="blue",bg="white",font=("Arial",15,"bold"))
show_attendance=Button(window.frame,text="View Attendance",command=call_view_attendance,activebackground="blue"
                       ,activeforeground="white",fg="blue",bg="white",font=("Arial",15,"bold"))

# positioning buttons
user_registration.place(x=10,y=10,width=300)
Take_attendance.place(x=80,y=125,width=300)
delete_user.place(x=185,y=240,width=300)
show_attendance.place(x=285,y=345,width=300)

# looping through window
window.mainloop()

