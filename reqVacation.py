#!/usr/bin/env python3

from tkinter import *
from tkinter import messagebox
import shelve
from modCalendar import *
from userConfig import *

class loginSys(Frame):
    def __init__(self,master):
        Frame.__init__(self,master,pady=10)
        self.grid(row=0,column=0)
        self.createWidgets()

    def checkUser(self):
        user,pwd=self.userName.get().strip(),self.password.get().strip()
        authMsg=user + " " + pwd
        db=shelve.open("staffDB")

        if authMsg == db[user].userName+" "+db[user].passWord:
            app=calApp(self,currentYear,currentMonth,currentTime)
            info=infoPanel(self,db[user].firstName+" "+db[user].lastName,db[user])

        else:
            messagebox.showwarning("Warning","Invalid Username/Password")

    def quit(self):
        root.quit()
        root.destroy()
        exit()

    def createWidgets(self):
        self.loginTitle=Label(self,text="Department Vacation System",anchor=CENTER,font=("tahoma","18","bold"),padx=10,pady=15)
        self.loginTitle.grid(row=0,column=0)
        self.loginTitle.configure(foreground="red")

        self.lbFrame=LabelFrame(self,padx=10)
        self.lbFrame.grid(row=1,column=0,columnspan=2)

        self.usrName=Label(self.lbFrame,text="Username: ",font=("tahoma","10","bold"),padx=10,pady=10)
        self.usrName.grid(row=0,column=0,sticky="e")

        self.userName=StringVar()
        self.nameEntry=Entry(self.lbFrame,width=15,textvariable=self.userName)
        self.nameEntry.grid(row=0,column=1)

        self.userPass=Label(self.lbFrame,text="Password: ",font=("tahoma","10","bold"),padx=10,pady=10)
        self.userPass.grid(row=1,column=0,sticky="e")

        self.password=StringVar()
        self.passEntry=Entry(self.lbFrame,width=15,textvariable=self.password,show="*")
        self.passEntry.grid(row=1,column=1)

        self.buttonFrame=Frame(self.lbFrame,padx=10)
        self.buttonFrame.grid(row=2,column=0,columnspan=2)

        self.logButton=Button(self.buttonFrame,width=6,text="Login",command=self.checkUser)
        self.logButton.grid(row=0,column=0,columnspan=2)

        self.quitButton=Button(self.buttonFrame,width=6,text="Quit",command=self.quit)
        self.quitButton.grid(row=0,column=2,columnspan=2)

if __name__ == "__main__":
    root=Tk()
    root.title("Department")
    login=loginSys(root)
    root.mainloop()
