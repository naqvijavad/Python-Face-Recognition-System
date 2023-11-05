# Importing required packages
import os
import csv
import tkinter
from tkinter import *
from tkinter import messagebox
import projectmodules as pm
import re
import shutil
from PIL import ImageTk

window=Tk()   # creating a window name window

def goto_back():
    """This function is used to go to maingui and destroy the current window"""
    window.destroy()
    os.system('maingui.py')


def goto_viewemp():
    """This function is used to view the employee data"""
    emp_file=r'.\Datafiles\EmployeeData.xlsx'
    os.startfile(emp_file)


def goto_deletedusersdata():
    """This function is used to view the deleted users data excel file"""
    dele_file=r'.\Datafiles\Deletedusersdata.xlsx'
    os.startfile(dele_file)


def goto_del():
    """This function validates the input and then deleting user data from employee file and attendance report file
        and also deleting saved images of user and then again training user data"""
    name=ename.get()  # storing name from entry
    id=eid.get()  # storing id from entry

    excelfile_empdata=r'.\Datafiles\EmployeeData.xlsx'
    excelfile_areport=r'.\Datafiles\AttendanceReport.xlsx'
    csvfile_empdata=r'.\Datafiles\EmployeeData.csv'
    csvfile_areport=r'.\Datafiles\AttendanceReport.csv'
    excelfile_deletedusers = r'.\Datafiles\Deletedusersdata.xlsx'
    csvfile_deletedusers = r'.\Datafiles\Deletedusersdata.csv'

    res_name = bool(re.search(r'\d', name))  # regular expression search for is there is any digit in name
    res_id = id.isdigit()   # returns True if all the characters are digits

    # returns True if all the characters in a string are not whitespaces and name is also not empty
    res_name_empty = bool(name and not name.isspace())
    res_eid_empty = bool(id and not id.isspace())
    directory=f".\Dataset\{id}"  # directory of deleting user
    if res_name_empty == False or res_eid_empty == False:  # if name or id is empty
        tkinter.messagebox.showerror(title="Error", message="Cannot leave a field blank")  # display error
    elif res_name == True or res_id == False:  # if name contains a digit or id contains a character
        tkinter.messagebox.showerror(title="Error", message="Please enter correct data")  # display error
    else:
        flag=0
        newlines=[]  # creating a empty list
        del_lines=[]  # creating empty list for deleted user
        pm.from_excel_to_csv(excelfile_empdata,csvfile_empdata)  # converting from excel to csv of empdata file
        # converting from excel to csv of attendance report file
        pm.from_excel_to_csv(excelfile_areport,csvfile_areport)
        pm.from_excel_to_csv(excelfile_deletedusers, csvfile_deletedusers)
        with open(csvfile_deletedusers,'r') as k:  # reading the deleted user data file
            data=csv.reader(k)
            del_lines=list(data)
        with open(csvfile_empdata,'r') as f:  # reading the employee data file
            data=csv.reader(f)
            lines=list(data)
            for line in lines:
                if line[1]==id and line[2]==name:  # line list at 1 and at 2 is equal to id and name
                    flag=1
                    continue
                newlines.append(line)   # appending the line in newlines list
        with open(csvfile_empdata,'w') as g:  # opening employee data file in write mode
            writer=csv.writer(g,lineterminator='\n')
            writer.writerows(newlines)
        newlines.clear()

        with open(csvfile_areport,'r') as f:  # reading the attendance report file
            data=csv.reader(f)
            lines=list(data)
            del_lines[0]=lines[0]
            for line in lines:
                if line[1]==id and line[2]==name:  # line list at 1 and at 2 is equal to id and name
                    flag=1
                    del_lines.append(line)
                    continue
                newlines.append(line)

        with open(csvfile_areport,'w') as g:     # opening attendance report file in write mode
            writer=csv.writer(g,lineterminator='\n')
            writer.writerows(newlines)

        if flag==1:
            pm.update_excel(csvfile_empdata,excelfile_empdata)  # updating the employee data excel to csv file
            pm.update_excel(csvfile_areport,excelfile_areport)  # updating the attendance report excel to csv file

            with open(csvfile_deletedusers,'w') as k:
                writer=csv.writer(k,lineterminator='\n')
                writer.writerows(del_lines)
            pm.update_excel(csvfile_deletedusers,excelfile_deletedusers)
            try:
                shutil.rmtree(directory)  # removing the directory of deleting user
                excelfile = r'.\Datafiles\EmployeeData.xlsx'
                csvfile = r'.\Datafiles\EmployeeData.csv'
                pm.from_excel_to_csv(excelfile, csvfile)  # converting excel to csv
                names = pm.get_employee_data(csvfile)  # getiing employee data in names dictionary
                ask = len(names.keys())
                if ask==0:
                    recogfile=r'.\Recognizer\Trained_data.yml'
                    os.remove(recogfile)
                else:
                    os.system('TrainingData.py')  # redirecting to training data
                result = Label(window.frame, text="User Deleted Successfully",bg="white"
                             ,fg="blue",font=("Arial",12,"bold"))  # displaying user deleted successfully
                result.place(x=10, y=300, width=400)
            except:
                result=Label(window.frame,text="User Directory not found",bg="white"
                             ,fg="blue",font=("Arial",12,"bold"))  # displaying user directory not found
                result.place(x=10, y=300, width=400)
        else:
            result=Label(window.frame,text="User Not found",bg="white"
                             ,fg="blue",font=("Arial",12,"bold"))  # displaying user not found
            result.place(x=10, y=300, width=400)


window.geometry("1200x700+150+50")  # creating window with 1200px width 700px height and 150 from x axis and 50 from y
window.title("DELETE USER")  # giving title to window
window.resizable(width=False,height=False)  # setting width and height non-resizeable

bkimage=ImageTk.PhotoImage(file="./Images/background1.jpg")
imglbl=Label(window,image=bkimage)   # setting image as label in background
imglbl.pack()  # packing the image label

window.frame=Frame(window,background="black")  # creating a frame in window with black background
window.frame.place(x=315,y=150,width=600,height=400)  # assigning the frame at given co-ordinates

# creating labels
name_lbl=Label(window.frame,text="Enter Employee Name : ",bg="white",fg="blue",font=("Arial",12,"bold"))
id_lbl=Label(window.frame,text="Enter employee id : ",bg="white",fg="blue",font=("Arial",12,"bold"))

# positioning labels
name_lbl.place(x=10,y=10,width=200)
id_lbl.place(x=10,y=80,width=200)

# crating entry to get input from user
ename=Entry(window.frame,bg="white",fg="blue",font=("Arial",12,"bold"))
eid=Entry(window.frame,bg="white",fg="blue",font=("Arial",12,"bold"))

# positioning entry
ename.place(x=240,y=10,width=200)
eid.place(x=240,y=80,width=200)

# creating buttons
bk_btn=Button(window.frame,text="BACK",command=goto_back,activebackground="blue"
                           ,activeforeground="white",fg="blue",bg="white",font=("Arial",12,"bold"))
del_btn=Button(window.frame,text="DELETE",command=goto_del,activebackground="blue"
                           ,activeforeground="white",fg="blue",bg="white",font=("Arial",12,"bold"))
view_del_users=Button(window.frame,text="View Deleted Users Data",command=goto_deletedusersdata
                      ,activebackground="blue",activeforeground="white",fg="blue",bg="white",font=("Arial",12,"bold"))
view_emp_data=Button(window.frame,text="View Employee",command=goto_viewemp,activebackground="blue"
                     ,activeforeground="white",fg="blue",bg="white",font=("Arial",12,"bold"))

# positioning buttons
bk_btn.place(x=10,y=200,width=200)
del_btn.place(x=240,y=200,width=200)
view_del_users.place(x=10,y=260,width=200)
view_emp_data.place(x=240,y=260,width=200)

# looping through window
window.mainloop()