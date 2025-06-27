from tkinter import *
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
enrolledrec = [[]]
current_value = ''
subjarr = ''
subjtemp = ''

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
    creategrid2()

def callback2(event):
    li = []
    li=event.widget._values
    global subjtemp
    subjtemp = enrolledrec[li[1]][0]
    
def deletegrid():
    for label in window.grid_slaves():
        if (int(label.grid_info()["row"]) > 7) and int(label.grid_info()["column"]) > 3:
            label.grid_forget()

def deletegrid2():
    for label in window.grid_slaves():
        if (int(label.grid_info()["row"]) > 7) and int(label.grid_info()["column"]) > 9:
            label.grid_forget()
            
def creategrid():
    deletegrid()
    global studrec, current_value
    temp = filter_idNumEntry.get().isnumeric()
    if current_value == '>' and temp:
         student = mycol.aggregate([{"$match":{"studid":{"$gt":int(filter_idNumEntry.get())},
        "studname": {"$regex": "^"+filter_nameStartEntry.get()+".*"+filter_nameEndEntry.get()+"$"},
        "studemail":{"$regex": "^"+filter_mailEntry.get()}, "studcourse":{"$regex": "^"+filter_courseEntry.get()}}},
                                   {"$lookup":{"from":"subjects","localField":"subjid","foreignField":"subjid","as":"enrolled"}},
                                   {"$unwind": {"path":"$enrolled", "preserveNullAndEmptyArrays":True}},
                                   {"$group":{"_id":"$_id","studid":{"$first":"$studid"},"studname":{"$first":"$studname"},
                                    "studemail": {"$first": "$studemail"},  
                                    "studcourse": {"$first": "$studcourse"},  
                                    "totunits":{"$sum": {"$toInt":"$enrolled.subjunits"}}}},{"$sort": {"studid": 1}}])
    elif current_value == '<' and temp:
         student = mycol.aggregate([{"$match":{"studid":{"$lt":int(filter_idNumEntry.get())},
        "studname": {"$regex": "^"+filter_nameStartEntry.get()+".*"+filter_nameEndEntry.get()+"$"},
        "studemail":{"$regex": "^"+filter_mailEntry.get()}, "studcourse":{"$regex": "^"+filter_courseEntry.get()}}},
                                   {"$lookup":{"from":"subjects","localField":"subjid","foreignField":"subjid","as":"enrolled"}},
                                   {"$unwind": {"path":"$enrolled", "preserveNullAndEmptyArrays":True}},
                                   {"$group":{"_id":"$_id","studid":{"$first":"$studid"},"studname":{"$first":"$studname"},
                                    "studemail": {"$first": "$studemail"},  
                                    "studcourse": {"$first": "$studcourse"},  
                                    "totunits":{"$sum": {"$toInt":"$enrolled.subjunits"}}}},{"$sort": {"studid": 1}}])
    elif current_value == '>=' and temp:
         student = mycol.aggregate([{"$match":{"studid":{"$gte":int(filter_idNumEntry.get())},
        "studname": {"$regex": "^"+filter_nameStartEntry.get()+".*"+filter_nameEndEntry.get()+"$"},
        "studemail":{"$regex": "^"+filter_mailEntry.get()}, "studcourse":{"$regex": "^"+filter_courseEntry.get()}}},
                                   {"$lookup":{"from":"subjects","localField":"subjid","foreignField":"subjid","as":"enrolled"}},
                                   {"$unwind": {"path":"$enrolled", "preserveNullAndEmptyArrays":True}},
                                   {"$group":{"_id":"$_id","studid":{"$first":"$studid"},"studname":{"$first":"$studname"},
                                    "studemail": {"$first": "$studemail"},  
                                    "studcourse": {"$first": "$studcourse"},  
                                    "totunits":{"$sum": {"$toInt":"$enrolled.subjunits"}}}},{"$sort": {"studid": 1}}])
    elif current_value == '<=' and temp:
        student = mycol.aggregate([{"$match":{"studid":{"$lte":int(filter_idNumEntry.get())},
        "studname": {"$regex": "^"+filter_nameStartEntry.get()+".*"+filter_nameEndEntry.get()+"$"},
        "studemail":{"$regex": "^"+filter_mailEntry.get()}, "studcourse":{"$regex": "^"+filter_courseEntry.get()}}},
                                   {"$lookup":{"from":"subjects","localField":"subjid","foreignField":"subjid","as":"enrolled"}},
                                   {"$unwind": {"path":"$enrolled", "preserveNullAndEmptyArrays":True}},
                                   {"$group":{"_id":"$_id","studid":{"$first":"$studid"},"studname":{"$first":"$studname"},
                                    "studemail": {"$first": "$studemail"},  
                                    "studcourse": {"$first": "$studcourse"},  
                                    "totunits":{"$sum": {"$toInt":"$enrolled.subjunits"}}}},{"$sort": {"studid": 1}}])
    elif current_value == '!=' and temp:
         student = mycol.aggregate([{"$match":{"studid":{"$ne":int(filter_idNumEntry.get())},
        "studname": {"$regex": "^"+filter_nameStartEntry.get()+".*"+filter_nameEndEntry.get()+"$"},
        "studemail":{"$regex": "^"+filter_mailEntry.get()}, "studcourse":{"$regex": "^"+filter_courseEntry.get()}}},
                                   {"$lookup":{"from":"subjects","localField":"subjid","foreignField":"subjid","as":"enrolled"}},
                                   {"$unwind": {"path":"$enrolled", "preserveNullAndEmptyArrays":True}},
                                   {"$group":{"_id":"$_id","studid":{"$first":"$studid"},"studname":{"$first":"$studname"},
                                    "studemail": {"$first": "$studemail"},  
                                    "studcourse": {"$first": "$studcourse"},  
                                    "totunits":{"$sum": {"$toInt":"$enrolled.subjunits"}}}},{"$sort": {"studid": 1}}])
    elif current_value == '=' and temp:
        student = mycol.aggregate([{"$match":{"studid":{"$eq":int(filter_idNumEntry.get())},
        "studname": {"$regex": "^"+filter_nameStartEntry.get()+".*"+filter_nameEndEntry.get()+"$"},
        "studemail":{"$regex": "^"+filter_mailEntry.get()}, "studcourse":{"$regex": "^"+filter_courseEntry.get()}}},
                                   {"$lookup":{"from":"subjects","localField":"subjid","foreignField":"subjid","as":"enrolled"}},
                                   {"$unwind": {"path":"$enrolled", "preserveNullAndEmptyArrays":True}},
                                   {"$group":{"_id":"$_id","studid":{"$first":"$studid"},"studname":{"$first":"$studname"},
                                    "studemail": {"$first": "$studemail"},  
                                    "studcourse": {"$first": "$studcourse"},  
                                    "totunits":{"$sum": {"$toInt":"$enrolled.subjunits"}}}},{"$sort": {"studid": 1}}])
    else:
        student = mycol.aggregate([{"$match":{"studname": {"$regex": "^"+filter_nameStartEntry.get()+".*"+filter_nameEndEntry.get()+"$"},
        "studemail":{"$regex": "^"+filter_mailEntry.get()}, "studcourse":{"$regex": "^"+filter_courseEntry.get()}}},
                                   {"$lookup":{"from":"subjects","localField":"subjid","foreignField":"subjid","as":"enrolled"}},
                                   {"$unwind": {"path":"$enrolled", "preserveNullAndEmptyArrays":True}},
                                   {"$group":{"_id":"$_id","studid":{"$first":"$studid"},"studname":{"$first":"$studname"},
                                    "studemail": {"$first": "$studemail"},  
                                    "studcourse": {"$first": "$studcourse"},  
                                    "totunits":{"$sum": {"$toInt":"$enrolled.subjunits"}}}},{"$sort": {"studid": 1}}])
    students = list(student)
    studrec = [[stud['studid'], stud['studname'], stud['studemail'], stud['studcourse'], stud['totunits']] for stud in students]
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
        mycol2.update_one({"subjid": int(subjid.get())}, {"$set":{"subjcode": subjcode.get()}})
        mycol2.update_one({"subjid": int(subjid.get())}, {"$set":{"subjdesc": subjdesc.get()}})
        mycol2.update_one({"subjid": int(subjid.get())}, {"$set":{"subjunits": subjunits.get()}})
        mycol2.update_one({"subjid": int(subjid.get())}, {"$set":{"subjsched": subjsched.get()}})
        creategrid()

def delete():
    r=msgbox("delete record","record")
    if r==True:
        mycol.delete_one({"studid": int(studid.get())})
        creategrid()

def addSub():
    r=msgbox("add subject","record")
    if r==True:
        mycol.update_one({"studid": int(studid.get())}, {"$push":{"subjid": subjarr}})
        creategrid()
        creategrid2()

def dropSub():
    r=msgbox("drop subject","record")
    if r==True:
        mycol.update_one({"studid": int(studid.get())}, {"$pull":{"subjid": subjtemp}})
        creategrid()
        creategrid2()

def creategrid2():
    deletegrid2()
    global enrolledrec
    subject = mycol.aggregate([{"$match":{"studid":int(studid.get())}},
                               {"$lookup":{"from":"subjects","localField":"subjid","foreignField":"subjid","as":"enrolled"}},
                               {"$unwind": "$enrolled"},
                               {"$project": {"subjid":"$enrolled.subjid", "subjcode":"$enrolled.subjcode", "subjdesc":"$enrolled.subjdesc","subjunits":"$enrolled.subjunits", "subjsched":"$enrolled.subjsched"}}])
    enrolled = list(subject)
    enrolledrec = [[sub['subjid'], sub['subjcode'], sub['subjdesc'], sub['subjunits'], sub['subjsched']] for sub in enrolled]
    for i in range(len(enrolledrec)):
        for j in range(len(enrolledrec[0])):
            mgrid = tk.Entry(window,width=15)
            mgrid.insert(tk.END, enrolledrec[i][j])
            mgrid._values = mgrid.get(), i
            mgrid.grid(row=i+8, column=j+10)
            mgrid.bind("<Button-1>", callback2)
            
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

#exer 5
addbtn = tk.Button(text="Add Subject", command=addSub)
addbtn.grid(column=2,row=8)

dropbtn = tk.Button(text = "Drop Subject", command=dropSub)
dropbtn.grid(column=3,row=8)

# subjtable

label = tk.Label(window, text="SubjID", width=13, height= 1, bg="yellow", anchor="center")
label.grid(column=10,row=7)

label = tk.Label(window, text="SubjCode", width=13, height= 1, bg="yellow", anchor="center")
label.grid(column=11,row=7)

label = tk.Label(window, text="SubjDesc", width=13, height= 1, bg="yellow", anchor="center")
label.grid(column=12,row=7)

label = tk.Label(window, text="SubjUnits", width=13, height= 1, bg="yellow", anchor="center")
label.grid(column=13,row=7)

label = tk.Label(window, text="SubjSched", width=13, height= 1, bg="yellow", anchor="center")
label.grid(column=14,row=7)

def createSubj(parent_window):
    window2 = tk.Toplevel(parent_window)
    window2.title("Subjects")
    window2.geometry("1050x400")
    window2.configure(bg="orange")

    mycol2 = mydb["subjects"]
    global subjrec
    subjrec = [[]]

    label = tk.Label(window2, text="Add Subjects", width=20, height= 1, bg="yellow", anchor="center")
    label.config(font=("Courier", 10))
    label.grid(column=2,row=1)

    label = tk.Label(window2, text="Subject ID", width=15, height= 1, bg="yellow", anchor="center")
    label.grid(column=1,row=2)

    label = tk.Label(window2, text="Subject Code", width=15, height= 1, bg="yellow", anchor="center")
    label.grid(column=1,row=3)

    label = tk.Label(window2, text="Subject Desc", width=15, height= 1, bg="yellow", anchor="center")
    label.grid(column=1,row=4)

    label = tk.Label(window2, text="Subject Units", width=15, height= 1, bg="yellow", anchor="center")
    label.grid(column=1,row=5)
    
    label = tk.Label(window2, text="Subject Sched", width=15, height= 1, bg="yellow", anchor="center")
    label.grid(column=1,row=6)

    subid = tk.StringVar()
    subjid = tk.Entry(window2, textvariable=subid)
    subjid.grid(column=2,row=2)
    
    subcode = tk.StringVar()
    subjcode = tk.Entry(window2, textvariable=subcode)
    subjcode.grid(column=2,row=3)

    subdesc = tk.StringVar()
    subjdesc = tk.Entry(window2, textvariable=subdesc)
    subjdesc.grid(column=2,row=4)

    subunits = tk.StringVar()
    subjunits = tk.Entry(window2, textvariable=subunits)
    subjunits.grid(column=2,row=5)

    subsched = tk.StringVar()
    subjsched = tk.Entry(window2, textvariable=subsched)
    subjsched.grid(column=2,row=6)

    def msgbox(msg,titlebar):
        result=messagebox.askokcancel(title=titlebar, message=msg)
        return result

    def callback2(event):
        li = []
        li=event.widget._values
        subid.set(subjrec[li[1]][0])
        global subjarr
        subjarr = subjrec[li[1]][0]
        subcode.set(subjrec[li[1]][1])
        subdesc.set(subjrec[li[1]][2])
        subunits.set(subjrec[li[1]][3])
        subsched.set(subjrec[li[1]][4])
        
    def deletegrid():
        for label in window2.grid_slaves():
            if (int(label.grid_info()["row"]) > 8) and int(label.grid_info()["column"]) > 3:
                label.grid_forget()
    def creategrid():
        deletegrid()
        global subjrec
        subjects = list(mycol2.find({}))
        subjrec = [[sub['subjid'], sub['subjcode'], sub['subjdesc'], sub['subjunits'], sub['subjsched']] for sub in subjects]
        
        for i in range(len(subjrec)):
            for j in range(len(subjrec[0])):
                mgrid = tk.Entry(window2,width=15)
                mgrid.insert(tk.END, subjrec[i][j])
                mgrid._values = mgrid.get(), i
                mgrid.grid(row=i+9, column=j+4)
                mgrid.bind("<Button-1>",  callback2)
    def save():
        r=msgbox("save record","record")
        if r==True:
            mycol2.insert_one({"subjid": int(subjid.get()),"subjcode": subjcode.get(), "subjdesc": subjdesc.get(), "subjunits": subjunits.get(),"subjsched": subjsched.get()})
            creategrid()

    def update():
        r=msgbox("update record","record")
        if r==True:
            mycol2.update_one({"subjid": int(studid.get())}, {"$set":{"subjcode": studname.get()}})
            mycol2.update_one({"subjid": int(studid.get())}, {"$set":{"subjdesc": studadd.get()}})
            mycol2.update_one({"subjid": int(studid.get())}, {"$set":{"subjunits": studcourse.get()}})
            mycol2.update_one({"subjid": int(studid.get())}, {"$set":{"subjsched": studcourse.get()}})
            creategrid()

    def delete():
        r=msgbox("delete record","record")
        if r==True:
            mycol2.delete_one({"subjid": int(subjid.get())})
            creategrid()
    
    savebtn = tk.Button(window2, text="Save", command=save)
    savebtn.grid(column=1,row=7)

    deletebtn = tk.Button(window2, text = "Delete", command=delete)
    deletebtn.grid(column=2,row=7)

    updatebtn = tk.Button(window2, text = "Update", command=update)
    updatebtn.grid(column=3,row=7)

    # table

    label = tk.Label(window2, text="SubjID", width=13, height= 1, bg="yellow", anchor="center")
    label.grid(column=4,row=8)

    label = tk.Label(window2, text="SubjCode", width=13, height= 1, bg="yellow", anchor="center")
    label.grid(column=5,row=8)

    label = tk.Label(window2, text="SubjDesc", width=13, height= 1, bg="yellow", anchor="center")
    label.grid(column=6,row=8)

    label = tk.Label(window2, text="SubjUnits", width=13, height= 1, bg="yellow", anchor="center")
    label.grid(column=7,row=8)

    label = tk.Label(window2, text="SubjSched", width=13, height= 1, bg="yellow", anchor="center")
    label.grid(column=8,row=8)

    creategrid()
    window2.mainloop()
    
menubar = Menu(window)
window.config(menu=menubar)
file = Menu(menubar, tearoff = 0) 
menubar.add_cascade(label ='File', menu = file) 
file.add_command(label ='Subjects', command = lambda: createSubj(window))
file.add_separator() 
file.add_command(label ='Exit', command = window.destroy) 

creategrid()
window.mainloop()
