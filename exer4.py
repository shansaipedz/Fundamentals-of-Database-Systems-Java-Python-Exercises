import tkinter as tk
from tkinter import ttk
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
result = mycol.find({})
current_value = ''

label = tk.Label(window, text="Student Registration", width=20, height= 1, bg="yellow", anchor="center")
label.config(font=("Courier", 10))
label.grid(column=2,row=1)

label = tk.Label(window, text="Student ID:", width=15, height= 1, bg="yellow", anchor="center")
label.grid(column=1,row=2)

label = tk.Label(window, text="Student Name:", width=15, height= 1, bg="yellow", anchor="center")
label.grid(column=1,row=3)

label = tk.Label(window, text="Student Email:", width=15, height= 1, bg="yellow", anchor="center")
label.grid(column=1,row=4)

label = tk.Label(window, text="Student Course:", width=15, height= 1, bg="yellow", anchor="center")
label.grid(column=1,row=5)



# table

label = tk.Label(window, text="ID", width=13, height= 1, bg="yellow", anchor="center")
label.grid(column=4,row=7)

label = tk.Label(window, text="Name", width=13, height= 1, bg="yellow", anchor="center")
label.grid(column=5,row=7)

label = tk.Label(window, text="Email", width=13, height= 1, bg="yellow", anchor="center")
label.grid(column=6,row=7)

label = tk.Label(window, text="Course", width=13, height= 1, bg="yellow", anchor="center")
label.grid(column=7,row=7)

label = tk.Label(window, text="TotalUnits", width=13, height= 1, bg="yellow", anchor="center")
label.grid(column=8,row=7)

sid = tk.StringVar()
studid = tk.Entry(window, textvariable=sid)
studid.grid(column=2,row=2)

sname = tk.StringVar()
studname = tk.Entry(window, textvariable=sname)
studname.grid(column=2,row=3)

semail = tk.StringVar()
studemail = tk.Entry(window, textvariable=semail)
studemail.grid(column=2,row=4)

scourse = tk.StringVar()
studcourse = tk.Entry(window, textvariable=scourse)
studcourse.grid(column=2,row=5)

def msgbox(msg,titlebar):
    result=messagebox.askokcancel(title=titlebar, message=msg)
    return result

def callback(event):
    li = []
    li=event.widget._values
    sid.set(studrec[li[1]][0])
    sname.set(studrec[li[1]][1])
    semail.set(studrec[li[1]][2])
    scourse.set(studrec[li[1]][3])
    
def deletegrid():
    for label in window.grid_slaves():
        if (int(label.grid_info()["row"]) > 7):
            label.grid_forget()
def creategrid():
    deletegrid()
    global studrec, current_value
    temp = filter_idNumEntry.get().isnumeric()

    if current_value == '>' and temp:
        student = mycol.find({"studid": {"$gt": int(filter_idNumEntry.get())},
        "studname": {"$regex": "^"+filter_nameStartEntry.get()+".*"+filter_nameEndEntry.get()+"$"},
        "studemail":{"$regex": "^"+filter_mailEntry.get()}, "studcourse":{"$regex": "^"+filter_courseEntry.get()}})
    elif current_value == '<' and temp:
        student = mycol.find({"studid":{"$lt":int(filter_idNumEntry.get())},
        "studname": {"$regex": "^"+filter_nameStartEntry.get()+".*"+filter_nameEndEntry.get()+"$"},
        "studemail":{"$regex": "^"+filter_mailEntry.get()}, "studcourse":{"$regex": "^"+filter_courseEntry.get()}})
    elif current_value == '>=' and temp:
        student = mycol.find({"studid":{"$gte":int(filter_idNumEntry.get())},
        "studname": {"$regex": "^"+filter_nameStartEntry.get()+".*"+filter_nameEndEntry.get()+"$"},
        "studemail":{"$regex": "^"+filter_mailEntry.get()}, "studcourse":{"$regex": "^"+filter_courseEntry.get()}})
    elif current_value == '<=' and temp:
        student = mycol.find({"studid":{"$lte":int(filter_idNumEntry.get())},
        "studname": {"$regex": "^"+filter_nameStartEntry.get()+".*"+filter_nameEndEntry.get()+"$"},
        "studemail":{"$regex": "^"+filter_mailEntry.get()}, "studcourse":{"$regex": "^"+filter_courseEntry.get()}})
    elif current_value == '!=' and temp:
        student = mycol.find({"studid":{"$ne":int(filter_idNumEntry.get())},
        "studname": {"$regex": "^"+filter_nameStartEntry.get()+".*"+filter_nameEndEntry.get()+"$"},
        "studemail":{"$regex": "^"+filter_mailEntry.get()}, "studcourse":{"$regex": "^"+filter_courseEntry.get()}})
    elif current_value == '=' and temp:
        student = mycol.find({"studid":{"$eq":int(filter_idNumEntry.get())},
        "studname": {"$regex": "^"+filter_nameStartEntry.get()+".*"+filter_nameEndEntry.get()+"$"},
        "studemail":{"$regex": "^"+filter_mailEntry.get()}, "studcourse":{"$regex": "^"+filter_courseEntry.get()}})
    else:
        student = mycol.find({"studname": {"$regex": "^"+filter_nameStartEntry.get()+".*"+filter_nameEndEntry.get()+"$"},
        "studemail":{"$regex": "^"+filter_mailEntry.get()}, "studcourse":{"$regex": "^"+filter_courseEntry.get()}})
    students = list(student)
    studrec = [[stud['studid'], stud['studname'], stud['studemail'], stud['studcourse'], 0] for stud in students]
    for i in range(len(studrec)):
        for j in range(len(studrec[0])):
            mgrid = tk.Entry(window,width=15)
            mgrid.insert(tk.END, studrec[i][j])
            mgrid._values = mgrid.get(), i
            mgrid.grid(row=i+8, column=j+4)
            mgrid.bind("<Button-1>", callback)
def save():
    r=msgbox("save record","record")
    if r==True:
        mycol.insert_one({"studid": int(studid.get()),"studname": studname.get(), "studemail": studemail.get(), "studcourse": studcourse.get()})
        creategrid()

def update():
    r=msgbox("update record","record")
    if r==True:
        mycol.update_one({"studid": int(studid.get())}, {"$set":{"studname": studname.get()}})
        mycol.update_one({"studid": int(studid.get())}, {"$set":{"studemail": studemail.get()}})
        mycol.update_one({"studid": int(studid.get())}, {"$set":{"studcourse": studcourse.get()}})
        creategrid()

def delete():
    r=msgbox("delete record","record")
    if r==True:
        mycol.delete_one({"studid": int(studid.get())})
        creategrid()

savebtn = tk.Button(text="Save", command=save)
savebtn.grid(column=1,row=6)

deletebtn = tk.Button(text = "Delete", command=delete)
deletebtn.grid(column=2,row=6)

updatebtn = tk.Button(text = "Update", command=update)
updatebtn.grid(column=3,row=6)

#exer4

#row3
label = tk.Label(window, text="Filter:", width=10, height= 1, bg="yellow", anchor="center")
label.grid(column=4,row=3)

label = tk.Label(window, text="Name Start:", width=10, height= 1, bg="yellow", anchor="center")
label.grid(column=5,row=3)

#row4
label = tk.Label(window, text="ID:", width=10, height= 1, bg="yellow", anchor="center")
label.grid(column=4,row=4)

filter_nameStart = tk.StringVar()
filter_nameStartEntry = tk.Entry(window, textvariable=filter_nameStart, width=12)
filter_nameStartEntry.grid(column=5,row=4)

#row5
current_var = tk.StringVar()
def selection(e):
    global current_value
    current_value = e
dropdown = tk.OptionMenu(window, current_var, '>', '<', '>=', '<=', '=', '!=', command=selection)
dropdown.grid(column=4, row=5)

label = tk.Label(window, text="Name End:", width=10, height= 1, bg="yellow", anchor="center")
label.grid(column=5,row=5)

label = tk.Label(window, text="Mail Start:", width=10, height= 1, bg="yellow", anchor="center")
label.grid(column=6,row=5)

label = tk.Label(window, text="Course Start:", width=10, height= 1, bg="yellow", anchor="center")
label.grid(column=7,row=5)

#row6
filter_idNum = tk.StringVar()
filter_idNumEntry = tk.Entry(window, textvariable=filter_idNum, width=12)
filter_idNumEntry.grid(column=4,row=6)

filter_nameEnd = tk.StringVar()
filter_nameEndEntry = tk.Entry(window, textvariable=filter_nameEnd, width=12)
filter_nameEndEntry.grid(column=5,row=6)

filter_mail = tk.StringVar()
filter_mailEntry = tk.Entry(window, textvariable=filter_mail, width=12)
filter_mailEntry.grid(column=6,row=6)

filter_course = tk.StringVar()
filter_courseEntry = tk.Entry(window, textvariable=filter_course, width=12)
filter_courseEntry.grid(column=7,row=6)

filterbtn = tk.Button(text = "Filter", command=creategrid)
filterbtn.grid(column=9,row=6)

creategrid()
window.mainloop()
