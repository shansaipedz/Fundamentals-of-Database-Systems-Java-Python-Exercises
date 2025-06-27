import tkinter as tk 
from tkinter import messagebox
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["enrollmentsystems"]
mycol = mydb["students"]

windows = tk.Tk()
windows.title("Python Window")
windows.geometry("1050x400")
windows.configure(bg="orange")

label = tk.Label(windows, text="Student Registration", width=30, height=1, bg="yellow", anchor="center")
label.config(font=("Courier", 10))
label.grid(row=1, column=2)

label = tk.Label(windows, text="Student ID: ", width=10, height=1, bg="yellow")
label.grid(row=2, column=1)

label = tk.Label(windows, text="Student Name: ", width=10, height=1, bg="yellow")
label.grid(row=3, column=1)

label = tk.Label(windows, text="Student Address: ", width=10, height=1, bg="yellow")
label.grid(row=4, column=1)

label = tk.Label(windows, text="Student Contact: ", width=10, height=1, bg="yellow")
label.grid(row=5, column=1)

label = tk.Label(windows, text="Student Course: ", width=10, height=1, bg="yellow")
label.grid( row=6, column=1)

label = tk.Label(windows, text="Student Year Lvl: ", width=10, height=1, bg="yellow")
label.grid(row=7, column=1)

###Table Labels for the table later###
label = tk.Label(windows, text="Student ID", width=10, height=1, bg="yellow")
label.grid(row=8, column=5)

label = tk.Label(windows, text="Student Name", width=15, height=1, bg="yellow")
label.grid(row=8, column=6)

label = tk.Label(windows, text="Student Address", width=15, height=1, bg="yellow")
label.grid(row=8, column=7)

label = tk.Label(windows, text="Student Contact No.", width=15, height=1, bg="yellow")
label.grid(row=8, column=8)

label = tk.Label(windows, text="Student Course", width=15, height=1, bg="yellow")
label.grid(row=8, column=9)

label = tk.Label(windows, text="Student Year Level", width=15, height=1, bg="yellow")
label.grid(row=8, column=10)


###continue###

###textfields###
sID=tk.StringVar()
stud_id = tk.Entry(windows, textvariable=sID)
stud_id.grid(row=2, column=2)

sName=tk.StringVar()
stud_name = tk.Entry(windows, textvariable=sName)
stud_name.grid(row=3, column=2)

sAddress=tk.StringVar()
stud_address = tk.Entry(windows, textvariable=sAddress)
stud_address.grid(row=4, column=2)

sContactNum=tk.StringVar()
stud_contactnum = tk.Entry(windows, textvariable=sContactNum)
stud_contactnum.grid(row=5, column=2)

sCourse=tk.StringVar()
stud_course = tk.Entry(windows, textvariable=sCourse)
stud_course.grid(row=6, column=2)

sYrLvl=tk.StringVar()
stud_yrlvl = tk.Entry(windows, textvariable=sYrLvl)
stud_yrlvl.grid(row=7, column=2)

###continue###
studrec = [[]]

def callback(event):
    li=[]
    li=event.widget._values
    sID.set(studrec[li[1]][0])
    sName.set(studrec[li[1]][1])
    sAddress.set(studrec[li[1]][2])
    sContactNum.set(studrec[li[1]][3])
    sCourse.set(studrec[li[1]][4])
    sYrLvl.set(studrec[li[1]][5])

def creategrid(n):
    global studrec
    
    if n == 0:
        query={}
        students = list(mycol.find(query))
        studrec = [[std['studID'], std['studName'], std['studAddress'], 
                    std['studContactNumber'], std['studCourse'], 
                    std['studYrLvl']] for std in students]
        
        for i in range(len(studrec)):
            for j in range(len(studrec[0])):
                mygrid = tk.Entry(windows, width=10)
                mygrid.insert(tk.END, studrec[i][j])
                mygrid._values = mygrid.get(), i
                mygrid.grid(row=i+9, column=j+5)
                mygrid.bind("<Button-1>", callback)

    if n == 1:
        for label in windows.grid_slaves():
            if (int(label.grid_info()["row"]) > 8):
                label.grid_forget() 

def msgbox(msg, titlebar):
    result = messagebox.askokcancel(title=titlebar, message=msg)
    return result

def save():
    r = msgbox("save record?", "record")
    if r == True:
        x = mycol.insert_one({"studID":int(stud_id.get()), "studName":stud_name.get(), 
                              "studAddress":stud_address.get(), "studContactNumber":stud_contactnum.get(),
                                "studCourse":stud_course.get(), "studYrLvl":stud_yrlvl.get() });
        creategrid(1)
        creategrid(0)



def delete():
    r = msgbox("delete record?", "record")
    if r == True:
        mycol.delete_one({"studID": int(stud_id.get())})

    creategrid(1)
    creategrid(0)


def update():
    r = msgbox("update record?", "record")
    if r == True:
        result = mycol.update_one(
            {"studID": int(stud_id.get())},
            {
                "$set": {
                    "studName": stud_name.get(),
                    "studAddress": stud_address.get(),
                    "studContactNumber": stud_contactnum.get(),
                    "studCourse": stud_course.get(),
                    "studYrLvl": stud_yrlvl.get()
                }
            }
        )
        creategrid(1)
        creategrid(0)

savebtn = tk.Button(text = "Save", command=save)
savebtn.grid(column=1, row=8)
deletebtn = tk.Button(text = "Delete", command=delete)
deletebtn.grid(column=2, row=8)
updatebtn = tk.Button(text = "Update", command=update)
updatebtn.grid(column=3, row=8)
creategrid(0)

windows.mainloop()

