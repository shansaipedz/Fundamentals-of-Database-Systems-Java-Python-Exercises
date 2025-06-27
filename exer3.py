import tkinter as tk
from tkinter import messagebox
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["enrollmentsystem"]
mycol = mydb["students"]

window = tk.Tk()
window.title("Python Window")
window.geometry("1050x400")
window.configure(bg="orange")

studrec = [[]]

label = tk.Label(window, text="Student Registration", width=20, height= 1, bg="yellow", anchor="center")
label.config(font=("Courier", 10))
label.grid(column=2,row=1)

label = tk.Label(window, text="Student ID:", width=20, height= 1, bg="yellow", anchor="center")
label.grid(column=1,row=2)

label = tk.Label(window, text="Student Name:", width=20, height= 1, bg="yellow", anchor="center")
label.grid(column=1,row=3)

label = tk.Label(window, text="Student Address:", width=20, height= 1, bg="yellow", anchor="center")
label.grid(column=1,row=4)

label = tk.Label(window, text="Student Contact:", width=20, height= 1, bg="yellow", anchor="center")
label.grid(column=1,row=5)

label = tk.Label(window, text="Student Course:", width=20, height= 1, bg="yellow", anchor="center")
label.grid(column=1,row=6)

label = tk.Label(window, text="Student Year Lvl:", width=20, height= 1, bg="yellow", anchor="center")
label.grid(column=1,row=7)

# table

label = tk.Label(window, text="Studid", width=13, height= 1, bg="yellow", anchor="center")
label.grid(column=5,row=9)

label = tk.Label(window, text="Studname", width=13, height= 1, bg="yellow", anchor="center")
label.grid(column=6,row=9)

label = tk.Label(window, text="Studadd", width=13, height= 1, bg="yellow", anchor="center")
label.grid(column=7,row=9)

label = tk.Label(window, text="Studcontact", width=13, height= 1, bg="yellow", anchor="center")
label.grid(column=8,row=9)

label = tk.Label(window, text="Studcourse", width=13, height= 1, bg="yellow", anchor="center")
label.grid(column=9,row=9)

label = tk.Label(window, text="Studyear", width=13, height= 1, bg="yellow", anchor="center")
label.grid(column=10,row=9)


sid = tk.StringVar()
studid = tk.Entry(window, textvariable=sid)
studid.grid(column=2,row=2)

sname = tk.StringVar()
studname = tk.Entry(window, textvariable=sname)
studname.grid(column=2,row=3)

sadd = tk.StringVar()
studadd = tk.Entry(window, textvariable=sadd)
studadd.grid(column=2,row=4)

scontact = tk.StringVar()
studcontact = tk.Entry(window, textvariable=scontact)
studcontact.grid(column=2,row=5)

scourse = tk.StringVar()
studcourse = tk.Entry(window, textvariable=scourse)
studcourse.grid(column=2,row=6)

studyr = tk.StringVar()
studyear = tk.Entry(window, textvariable=studyr)
studyear.grid(column=2,row=7)

def msgbox(msg,titlebar):
    result=messagebox.askokcancel(title=titlebar, message=msg)
    return result

def callback(event):
    li = []
    li=event.widget._values
    sid.set(studrec[li[1]][0])
    sname.set(studrec[li[1]][1])
    sadd.set(studrec[li[1]][2])
    scontact.set(studrec[li[1]][3])
    scourse.set(studrec[li[1]][4])
    studyr.set(studrec[li[1]][5])
    
def deletegrid():
    for label in window.grid_slaves():
        if (int(label.grid_info()["row"]) > 9):
            label.grid_forget()
def creategrid():
    global studrec
    students = list(mycol.find({}))
    studrec = [[stud['studid'], stud['studname'], stud['studadd'],stud['studcontact'], stud['studcourse'], stud['studyear']] for stud in students]
    for i in range(len(studrec)):
        for j in range(len(studrec[0])):
            mgrid = tk.Entry(window,width=15)
            mgrid.insert(tk.END, studrec[i][j])
            mgrid._values = mgrid.get(), i
            mgrid.grid(row=i+10, column=j+5)
            mgrid.bind("<Button-1>", callback)
def save():
    r=msgbox("save record","record")
    if r==True:
        mycol.insert_one({"studid": int(studid.get()),"studname": studname.get(), "studadd": studadd.get(), "studcontact": studcontact.get(), "studcourse": studcourse.get(), "studyear": studyear.get()})
        deletegrid()
        creategrid()

def update():
    r=msgbox("update record","record")
    if r==True:
        mycol.update_one({"studid": int(studid.get())}, {"$set":{"studname": studname.get()}})
        mycol.update_one({"studid": int(studid.get())}, {"$set":{"studadd": studadd.get()}})
        mycol.update_one({"studid": int(studid.get())}, {"$set":{"studcontact": studcontact.get()}})
        mycol.update_one({"studid": int(studid.get())}, {"$set":{"studcourse": studcourse.get()}})
        mycol.update_one({"studid": int(studid.get())}, {"$set":{"studyear": studyear.get()}})
        deletegrid()
        creategrid()
def delete():
    r=msgbox("delete record","record")
    if r==True:
        mycol.delete_one({"studid": int(studid.get())})
        deletegrid()
        creategrid()

savebtn = tk.Button(text="Save", command=save)
savebtn.grid(column=1,row=8)

deletebtn = tk.Button(text = "Delete", command=delete)
deletebtn.grid(column=2,row=8)

updatebtn = tk.Button(text = "Update", command=update)
updatebtn.grid(column=3,row=8)


creategrid()
window.mainloop()
