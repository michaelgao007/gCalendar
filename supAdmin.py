#!/usr/bin/env python3

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from modCalendar import *
from reqVacation import *
from userConfig import *
import shelve
import copy

class supLogin(loginSys):
    def __init__(self,master):
        loginSys.__init__(self,master)

    def checkUser(self):
        user,pwd=self.userName.get(),self.password.get()
        authMsg=user+" "+pwd
        db=shelve.open("staffDB")

        if authMsg == db[user].userName+" "+db[user].passWord and db[user].supervisor == db[user].firstName+" "+db[user].lastName:
            for child in self.winfo_children():
                child.destroy()

            app=calApp(self,currentYear,currentMonth,currentTime)
            info=supPanel(self)

        else:
            messagebox.showwarning("Warning","Invalid Username/Password")

    def quit(self):
        root.quit()
        root.destroy()
        exit()

class supPanel(LabelFrame):
    def __init__(self,master):
        LabelFrame.__init__(self,master,text="Supervisor Control Panel",font=("tahoma","12","bold"),pady=10)
        self.grid(row=1,column=0)
        self.createWidgets()

    def createWidgets(self):
        staffList=[]
        db=shelve.open("staffDB")
        labels={}
        txtVar={}
        buttons={}
        rowID=4
        colID=0

        def showInfo():
            txtVar["Status"].set("")
            operatorName=operator.get().split(",")[1][1].strip().lower()+operator.get().split(",")[0].strip().lower()
            db=shelve.open("staffDB")
            pendingDays=""
            self.pList.config(state="normal")
            self.pList.delete("1.0",END)

            for label in ["CarryOver","Entitlement","Taken"]:
                txtVar[label].set(getattr(db[operatorName],label))

            txtVar["Left"].set(db[operatorName].Left)

            for days in db[operatorName].requestDays:
                pendingDays=days+"\n"
                self.pList.insert(END,pendingDays)

            self.pList.config(state="disabled")
            db.close()

        def dayPlus(lbName):
            tmp=txtVar[lbName].get()
            tmp=tmp+1
            txtVar[lbName].set(str(tmp))

            tmpLeft=txtVar["CarryOver"].get()+txtVar["Entitlement"].get()-txtVar["Taken"].get()

            if txtVar["CarryOver"].get()+txtVar["Entitlement"].get() <= txtVar["Taken"].get():
                messagebox.showwarning("Warning","No Available Days Left!")

            else:
                txtVar["Left"].set(str(tmpLeft))

        def dayMinus(lbName):
            tmp=txtVar[lbName].get()
            tmp=tmp-1

            if tmp >= 0 and txtVar["CarryOver"].get()+txtVar["Entitlement"].get() > txtVar["Taken"].get():
                txtVar[lbName].set(str(tmp))
                tmp=txtVar["CarryOver"].get()+txtVar["Entitlement"].get()-txtVar["Taken"].get()

                if txtVar["CarryOver"].get()+txtVar["Entitlement"].get() <= txtVar["Taken"].get():

                    if tmpLeft == 0:
                        txtVar["Left"].set(str(tmpLeft))
                        messagebox.showwarning("Warning","No vailable Days Left!")

                else:
                    txtVar["Left"].set(str(tmpLeft))

            else:messagebox.showwarning("Warning","No Available Days Left!")

        def approve():
            operatorName=operator.get().split(",")[1][1].strip().lower()+operator.get().split(",")[0].strip().lower()

            db=shelve.open("staffDB",writeback=True)

            takenDays=len(list(set(db[operatorName].requestDays+db[operatorName].approvedDays)))
            txtVar["Taken"].set(takenDays)

            approvedDays=db[operatorName].requestDays

            daysLeft=str(db[operatorName].CarryOver+db[operatorName].Entitlement-takenDays)
            txtVar["Left"].set(daysLeft)

            db[operatorName].Taken=takenDays
            db[operatorName].Left=daysLeft
            db[operatorName].approvedDays=list(set(db[operatorName].approvedDays+approvedDays))
            db[operatorName].requestDays=[]

            db.close()

            self.pList.config(state="normal")
            self.pList.delete("1.0",END)
            self.pList.insert(END,"Vacation Request Processed. Done....")
            self.pList.config(state="disabled")

        def reject():
            operatorName=operator.get().split(",")[1][1].strip().lower()+operator.get().split(",")[0].strip().lower()

            db=shelve.open("staffDB",writeback=True)
            db[operatorName].rejectDays=copy.copy(db[operatorName].requestDays)
            db[operatorName].requestDays=[]
            db.close()

            self.pList.cofig(state="normal")
            self.pList.delet("1.0",END)
            self.pList.insert(END,"Vacation Request Rejected. Done....")
            self.pList.config(state="disabled")

        def updateInfo():
            database=shelve.open("staffDB",writeback=True)

            operatorName=operator.get().split(",")[1][1].stript().lower()+operator.get().split(",")[0].strip().lower()
            database[operatorName].CarryOver=txtVar["CarryOver"].get()
            database[operatorName].Entitlement=txtVar["Entitlement"].get()
            database[operatorName].Taken=txtVar["Taken"].get()
            database[operatorName].Left=txtVar["Left"].get()

            database.close()
            txtVar["Status"].set("Staff Info Updated To Database.")

        def viewHistory():
            operatorName=operator.get().split(",")[1][1].strip().lower()+operator.get().split(",")[0].strip().lower()

            database=shelve.open("staffDB",writeback=True)

            newWindow=Toplevel(self)
            newWindow.title("Request History - %s"%(database[operatorName].firtstName+" "+database[operatorName].lastName))
            newWindow.transient(self)

            historyFrame=LabelFrame(newWindow)
            historyFrame.grid(row=0,column=0)

            pendingLabel=Label(historyFrame,text="Pending Requests:",font=("tahoma","8","bold"),pady=6)
            pendingLabel.grid(row=1,column=0)
            pendingLabel.config(foreground="red")

            approvedLabel=Label(historyFrame,text="Approved Requests:",font=("tahoma","8","bold"),pady=6)
            approvedLabel.grid(row=1,column=1)
            approvedLabel.config(foreground="red")

            pendingList=scrolledtext.ScrooledText(historyFrame,width=20,pady=6,wrap=WORD,state="disabled")
            pendingList.grid(row=2,column=0)

            approvedList=scrolledtext.ScrolledText(historyFrame,width=20,pady=6,wrap=WORD,state="disabled")
            approvedList.grid(row=2,column=1)

            plist=database[operatorName].requestDays
            alist=database[operatorName].approvedDays
            database[operatorName].rejectDays=[]
            database.close()

            plist.sort()
            alist.sort()

            pString=""
            aString=""

            pendingList.config(state="normal")
            approvedList.config(state="normal")

            for day in plist:
                pString=day+"\n\n"
                pendingList.insert(END,pString)

            for day in alist:
                aString=day+"\n\n"
                approvedList.insert(END,aString)

            pendingList.config(state="disabled")
            approvedList.config(state="disabled")

        for staff in db.keys():
            staffList.append(db[staff].lastName+", "+db[staff].firstName)

        db.close()

        self.lbFrame=LabelFrame(self,font=("tahoma","12","bold"),pady=10)
        self.lbFrame.grid(row=1,column=0,rowspan=3)

        self.pLabel=Label(self.lbFrame,text="Pending Request",font=("tahoma","8","bold"),pady=10)
        self.pLabel.grid(row=2,column=0)
        self.pLabel.configure(foreground="red")

        self.pList=scrolledtext.ScrolledText(self.lbFrame,width=30,wrap=WORD,state="disabled")
        self.pList.grid(row=3,column=0)
        self.pList.bind("<1>",lambda event: self.pList.focus_set())

        self.tFrame=Frame(self,pady=10)
        self.tFrame.grid(row=1,column=1)

        self.sLabel=Label(self.tFrame,text="Operators List",font=("tahoma","10","bold"),pady=10)
        self.sLabel.grid(row=0,column=0)
        self.sLabel.configure(foreground="red")

        operator=StringVar()
        self.nameList=ttk.Combobox(self.tFrame,textvariable=operator)
        self.nameList['values']=tuple(staffList)
        self.nameList.grid(row=1,column=0)

        chkButton=Button(self.tFrame,text="Show Info",font=("tahoma","8","bold"),command=showInfo)
        chkButton.grid(row=1,column=1,sticky="e")

        self.rFrame=Frame(self,pady=10)
        self.rFrame.grid(row=2,column=1)

        for label in ["CarryOver","Entitlement"]:
            Label(self.rFrame,width=10,pady=6,text=label,anchor="e",font=("tahoma","10")).grid(row=rowID,column=colID,sticky="e")

            colID+=1

            txtVar[label]=IntVar()
            labels[label]=Label(self.rFrame,textvariable=txtVar[label],width=4,font=("tahoma","10"))
            labels[label].grid(row=rowID,column=colID)
            labels[label].configure(foreground="blue")

            colID+=1
            Label(self.rFrame,width=6,text="day(s)",font=("tahoma","10")).grid(row=rowID,column=colID)

            buttons[label+"plus"]=Button(self.rFrame,width=2,text="+",font=("bold"),command=lambda para=label:dayPlus(para))
            buttons[label+"plus"].grid(row=rowID,column=colID)

            colID+=1
            buttons[label+"minus"]=Button(self.rFrame,width=2,text="-",font=("bold"),command=lambda para=label:dayMinus(para))
            buttons[label+"minus"].grid(row=rowID,column=colID)

            rowID+=1
            colID=0

        for label in ["Taken","Left"]:
            Label(self.rFrame,width=10,pady=6,text=label,anchor="e",font=("tahomo","10")).grid(row=rowID,column=colID,sticky="e")

            colID+=1

            txtVar[label]=IntVar()
            labels[label]=Label(self.rFrame,textvariable=txtVar[label],width=4,font=("tahoma","10"))
            labels[label].grid(row=rowID,column=colID)
            labels[label].configure(foreground="blue")

            colID+=1
            Label(self.rFrame,width=6,text="day(s)",font=("tahoma","10")).grid(row=rowID,column=colID)

            rowID+=1
            colID=0

        bUpdate=Button(self.rFrame,text="Update Info",font=("tahoma","8","bold"),command=updateInfo)
        bUpdate.grid(row=rowID-1,column=3,columnspan=2)

        txtVar["Status"]=StringVar()
        lStatus=Label(self.rFrame,textvariable=txtVar["Status"],anchor=CENTER,font=("tahoma","8","bold"),padx=6,pady=8)
        lStatus.grid(row=rowID,column=0,columnspan=5,sticky="we")
        lStatus.configure(foreground="dark green")

        self.bFrame=Frame(self,pady=10)
        self.bFrame.grid(row=3,column=1)

        bApprove=Button(self.bFrame,width=10,text="Approve",font=("tahoma","8","bold"),padx=8,pady=8,command=approve)
        bApprove.grid(row=0,column=1)

        bReject=Button(self.bFrame,width=10,text="Reject",font=("tahoma","8","bold"),padx=8,pady=8,command=reject)
        bReject.grid(row=0,column=3)

        bViewHistory=Button(self.bFrame,width=10,text="View History",font=("tahoma","8","bold"),padx=8,pady=10,command=viewHistory)
        bViewHistory.grid(row=0,column=5)

if __name__=="__main__":
    root=Tk()
    root.title("Supervisor")
    login=supLogin(root)
    root.mainloop()
