# Importing Required packages
import csv
import os
import tkinter
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import projectmodules
from PIL import ImageTk
import pandas


modeexcel=r'.\Datafiles\modeofdetect.xlsx'
modecsv=r'.\Datafiles\modeofdetect.csv'
projectmodules.from_excel_to_csv(modeexcel,modecsv)
with open(modecsv,'r') as f:
    data=csv.reader(f)
    lines=list(data)
    for line in lines:
        line[1]='True'
        with open(modecsv,'w') as g:
            writer=csv.writer(g,lineterminator='\n')
            writer.writerow(line)
            break
projectmodules.update_excel(modecsv,modeexcel)
window=Tk()  # creating a window name window
window.geometry("1200x700+150+50")  # creating window with 1200px width 700px height and 150 from x axis and 50 from y
window.title("Take Attendance")  # giving title to window
window.resizable(height=False,width=False)  # setting width and height non-resizeable


def chk_date():
    """This function checks date and decide if the date is valid or if date is new, previous or current
        and write the date in attendance report file"""
    date_str=date_inp.get()
    date_format="%d %B, %Y"
    try:
        date_obj = datetime.strptime(date_str, date_format).date()  # converting string to date object
        excelfile_areport = r'.\Datafiles\AttendanceReport.xlsx'
        csvfile_areport = r'.\Datafiles\AttendanceReport.csv'
        projectmodules.from_excel_to_csv(excelfile_areport, csvfile_areport)  # converting excel to csvfile
        samedate = 0
        with open(csvfile_areport, 'r') as f:  # reading csvfile to check if date is new or existing
            data = csv.reader(f)
            lines = list(data)
            date_newformat = "%Y-%m-%d"
            for line in lines:
                if line[1] == "id":
                    if line[-1] == "Department":
                        date_obj = str(date_obj)
                        line.append(date_obj)
                        with open(csvfile_areport, 'w') as g:
                            writer = csv.writer(g, lineterminator='\n')
                            writer.writerows(lines)
                            break
                    else:
                        if datetime.strptime(line[-1], date_newformat).date() == date_obj:
                            samedate = 1  # if date is current
                        else:
                            for j in range(4, len(line)):
                                if datetime.strptime(line[j], date_newformat).date() == date_obj:
                                    samedate = 2  # if date is old/previous
                        if samedate == 0:  # if date is new
                            date_obj = str(date_obj)
                            line.append(date_obj)
                            with open(csvfile_areport, 'w') as g:
                                writer = csv.writer(g, lineterminator='\n')
                                writer.writerows(lines)
                                break

        if samedate == 0:  # if date is new
            projectmodules.update_excel(csvfile_areport,excelfile_areport)
            # updating the csv file and converting to excel file
            os.system('Detect.py')
            result = Label(window.frame, text="Attendance Marked Successfully", bg="white", fg="blue"
                           , font=("Arial", 12, "bold"))  # displaying if attendance marked successfully
            result.place(x=10, y=350, width=300)
        elif samedate == 1:  # if date is current
            projectmodules.update_excel(csvfile_areport, excelfile_areport)
            os.system('Detect.py')
            result = Label(window.frame, text="Attendance Marked Successfully", bg="white", fg="blue"
                           , font=("Arial", 12, "bold"))
            result.place(x=10, y=350, width=300)
        else:  # if date is old/previous
            tkinter.messagebox.showerror(title="Error",
                                         message="Previous Attendance cannot be marked")
    except:
        tkinter.messagebox.showerror(title="Error", message="The date input should be in "
                                                            "Correct Format \nEg. 15 August, 1947")



def go_to_maingui():
    """This function redirect to main gui and destroy the current window"""
    window.destroy()
    os.system('maingui.py')


def turbo_mode():
    """This function is used to make detection in turbo mode"""
    projectmodules.from_excel_to_csv(modeexcel, modecsv)
    with open(modecsv, 'r') as f:
        data1 = csv.reader(f)
        lines1 = list(data1)
        for line1 in lines1:
            line1[1] = 'False'
            with open(modecsv, 'w') as g:
                writer1 = csv.writer(g, lineterminator='\n')
                writer1.writerow(line1)
                break
    df = pandas.read_csv(modecsv)
    df.to_excel(modeexcel, index=False)
    tkinter.messagebox.showinfo(title="Mode",message="Turbo Mode is now on")


def normal_mode():
    """This function is used to make detection in normal mode"""
    projectmodules.from_excel_to_csv(modeexcel, modecsv)
    with open(modecsv, 'r') as f:
        data2 = csv.reader(f)
        lines2 = list(data2)
        for line2 in lines2:
            line2[1] = 'True'
            line2.pop(0)
            with open(modecsv, 'w') as g:
                writer2 = csv.writer(g)
                writer2.writerow(line2)
                break
    df = pandas.read_csv(modecsv)
    df.to_excel(modeexcel, index=False)
    tkinter.messagebox.showinfo(title="Mode",message="Turbo Mode is now off")


bkimage=ImageTk.PhotoImage(file="./Images/background1.jpg")
imglbl=Label(window,image=bkimage)  # setting image as label in background
imglbl.pack()  # packing the image label

window.frame=Frame(window,background="black")  # creating a frame in window with black background
window.frame.place(x=315,y=150,width=600,height=400)  # assigning the frame at given co-ordinates

# creating label and positioning the label
date_lbl=Label(window.frame,text="Enter Date : ",bg="white",fg="blue",font=("Arial",12,"bold"))
date_lbl.place(x=10,y=50,width=150)

# crating entry to get input from user and positioning the entry
date_inp=Entry(window.frame,bg="white",fg="blue",font=("Arial",12,"bold"))
date_inp.place(x=180,y=50,width=150)

# creating buttons
goto_main=Button(window.frame,text="BACK",command=go_to_maingui,activebackground="blue"
                           ,activeforeground="white",fg="blue",bg="white",font=("Arial",12,"bold"))
take_attendance=Button(window.frame,text="TAKE ATTENDANCE",command=chk_date,activebackground="blue"
                           ,activeforeground="white",fg="blue",bg="white",font=("Arial",12,"bold"))
turbomode_on=Button(window.frame,text="TURBO MODE",command=turbo_mode,activebackground="blue"
                           ,activeforeground="white",fg="blue",bg="white",font=("Arial",12,"bold"))
normalmode_on=Button(window.frame,text="NORMAL MODE",command=normal_mode,activebackground="blue"
                           ,activeforeground="white",fg="blue",bg="white",font=("Arial",12,"bold"))

# positioning buttons
goto_main.place(x=10,y=200,width=200)
take_attendance.place(x=250,y=200,width=200)
turbomode_on.place(x=10,y=280,width=200)
normalmode_on.place(x=250,y=280,width=200)

# looping through window
window.mainloop()
