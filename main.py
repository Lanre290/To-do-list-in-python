from tkinter import *
from functions import *
from PIL import ImageTk,Image
import tkinter.ttk as tk
import sqlite3


def addNewTask():
    root = Toplevel()
    root.title("Add new task")
    options = ['Low','Medium','High']
    optionSelected = StringVar()

    mainBody = Frame(root)
    mainBody.pack(ipady=10,ipadx = 10)
    label_1 = Label(mainBody,text = "Task")
    label_1.grid(row  = 0,column =0,pady = (10,6))
    entry_1 = tk.Entry(mainBody,width = 20,font = ("Calibri Light",16))
    entry_1.grid(row = 0,column = 1,pady = (10,6))

    label_2 = Label(mainBody,text = "Priority")
    label_2.grid(row  = 1,column = 0,pady = (0,6))
    entry_2 = tk.OptionMenu(mainBody,optionSelected,"-----",*options)
    entry_2.grid(row = 1,column = 1,pady = (0,6))

    def register():
        if optionSelected.get() == "Low":
            reg = lowTask(title = str(entry_1.get()))
            reg.register()
        if optionSelected.get() == "Medium":
            reg = mediumTask(title = str(entry_1.get()))
            reg.register()
        if optionSelected.get() == "High":
            reg = highTask(title = str(entry_1.get()))
            reg.register()
        root.destroy()
        loadTasks()

    submitImage = ImageTk.PhotoImage(Image.open('done.png').resize((30,30)))
    submitButton = Button(mainBody,image = submitImage,text = "  Submit",compound="left",height=34,width = 180,font = ("Calibri Light",19),foreground = "#0c46fa",relief = "flat",activeforeground="#0c46fa",background="#f9f9f9",activebackground="#f9f9f9",cursor = "hand2",command = register)
    submitButton.grid(row = 2,column = 0,columnspan=2,pady = (5,5))


    root.mainloop()

root = Tk()
root.title("To do list app")
root.config(background="#ffffff")
root.state("zoomed")

firstTime = True
cont = ""
err_:object = Label()


topSide = Frame()
topSide.pack(padx= (40,20),pady = (80,50),anchor=W)
bigLabel = Label(topSide,text = "TODO List Demo App",font = ("Calibri Light",25),background="#ffffff")
bigLabel.pack()

mainBody = Frame()
mainBody.pack()

buttonFrame = Frame(mainBody)
buttonFrame.pack(anchor = E)
addImage = ImageTk.PhotoImage(Image.open('plus.png').resize((30,30)))
addButton = Button(buttonFrame,image = addImage,text = "  Add new task",compound="left",height=34,width = 180,font = ("Calibri Light",19),foreground = "#0c46fa",relief = "flat",activeforeground="#0c46fa",background="#ffffff",activebackground="#f9f9f9",cursor = "hand2",command = addNewTask)
addButton.pack()

taskMainBody = Frame(bg = "#ffffff")
taskMainBody.pack(anchor= W)
titleFrame = Frame(taskMainBody)
titleFrame.pack(anchor=W,padx=(60,20))
id = Label(titleFrame,text = "#",width=3,bg = "#ffffff",font = ("Calibri Light",18))
id.grid(row = 0,column=0)
taskName = Label(titleFrame,text = "Task Name",width=20,bg = "#ffffff",font = ("Calibri Light",18))
taskName.grid(row = 0,column=1)
Status = Label(titleFrame,text = "Status",width=25,bg = "#ffffff",font = ("Calibri Light",18))
Status.grid(row = 0,column=2)
Edit = Label(titleFrame,text = "Mark",width=10,bg = "#ffffff",font = ("Calibri Light",18))
Edit.grid(row = 0,column=3)
remove = Label(titleFrame,text = "Remove",width=10,bg = "#ffffff",font = ("Calibri Light",18))
remove.grid(row = 0,column=4)


editImage = ImageTk.PhotoImage(Image.open('check-mark.png').resize((30,30)))
removeImage = ImageTk.PhotoImage(Image.open('dry-clean.png').resize((30,30)))
checkImage = ImageTk.PhotoImage(Image.open('error.png').resize((30,30)))

taskMain = Frame(taskMainBody,bg = "#ffffff")
taskMain.pack(anchor=W)

errImage = ImageTk.PhotoImage(Image.open('problem.png').resize((200,200)))
def loadTasks():
    global firstTime,taskMain,checkImage,cont,err_
    conn2= sqlite3.connect('database.db')

    checkIfTableExists()

    cursor2=conn2.cursor()
    cursor2.execute("SELECT *,oid FROM tasks")
    output = cursor2.fetchall()
    print("out",output)
    if len(output) < 1:
        err_.forget()
        err = Label(taskMain,image = errImage,text = "No task registered yet",bg = "#ffffff",compound="top",font = ("Calibri Light",17))
        err.pack(pady = (20,20),padx = (400,100))
        err_ = err
    else:
        err_.forget()
        if firstTime != True:
            cont.forget()
            taskMain = Frame(taskMainBody,bg = "#ffffff")
            taskMain.pack(anchor=W)

        # row = 0
        for i in range(len(output)):
            taskTitle = output[i][0]
            taskPriority = output[i][1]
            taskState = output[i][2]
            taskOid = output[i][3]

            taskCont = Frame(taskMain,bg = "#ffffff")
            taskCont.pack(anchor=W,padx=(60,20))
            id_ = Label(taskCont,text = taskOid,width=3,bg = "#ffffff",font = ("Calibri Light",18))
            id_.grid(row = 0,column=0)
            taskName_ = Label(taskCont,text = f"{taskTitle}",width=20,bg = "#ffffff",font = ("Calibri Light",18))
            taskName_.grid(row = 0,column=1)

            dummyEntry  = Entry()
            dummyEntry.insert(0,str(taskOid))

            color = ""
            text = ""

            if taskPriority == "low":
                color = "04de20"
            if taskPriority == "medium":
                color = "04e2bd"
            if taskPriority == "high":
                color = "ee0120"

            if taskState == "done":
                text = "Done"
                color = "04de20"
            else:
                text = taskPriority
            Status_ = Label(taskCont,text = f"{text}",width=25,bg = f"#ffffff",fg = f"#{color}",font = ("Calibri Light",18))
            Status_.grid(row = 0,column=2)

            def markTask(tkOid = taskOid):
                print(dummyEntry.get())
                if taskPriority == "low":
                    reg = lowTask(oid = tkOid)
                    reg.mark()
                if taskPriority == "medium":
                    reg = mediumTask(oid = tkOid)
                    reg.mark()
                if taskPriority == "high":
                    reg = highTask(oid = tkOid)
                    reg.mark()
                conn2= sqlite3.connect('database.db')
                cursor2=conn2.cursor()
                cursor2.execute("SELECT *,oid FROM tasks")
                output = cursor2.fetchall()
                loadTasks()
            
            Edit_ = Button(taskCont,bg = "#ffffff",font = ("Calibri Light",18),image = editImage,relief = "flat",cursor = "hand2",command = markTask)
            Edit_.grid(row = 0,column=3,padx = (50,10))

            def removeTask(tkOid = taskOid):
                pro = tasks(oid= tkOid)
                pro.remove()
                taskCont.forget()
                loadTasks()

            image = ""
            if taskState == "done":
                image = removeImage
            else:
                image = checkImage

            remove_ = Button(taskCont,text = "Remove",bg = "#ffffff",font = ("Calibri Light",18),image = image,cursor = "hand2",relief = "flat",command = removeTask)
            remove_.grid(row = 0,column=4,padx = (70,10))
            
            # row+=1

            

        cont = taskMain
        firstTime = False

loadTasks()


root.mainloop()