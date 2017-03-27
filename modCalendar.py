#!/usr/bin/env python3

from tkinter import *
from tkinter import scrolledtext
from time import *
from calendar import *
from datetime import datetime,timedelta
import shelve

currentTime=datetime.now().strftime("%Y %b").split()[1]
currentYear=int(datetime.now().strftime("%Y %m").split()[0])
currentMonth=int(datetime.now().strftime("%Y %m").split()[1])

class calApp(LabelFrame):
    def __init__(self,master,year,month,time):
        LabelFrame.__init__(self,master,text="Department Calendar",font=("tahoma","12","bold"),pady=10)
        self.grid(row=0,column=0)
        self.year=year
        self.month=month
        self.time=time
        self.monthList=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        self.createHeader(str(self.year)+" "+self.time)
        self.createWidgets(self.year,self.month)

    def createHeader(self,time):
        prevMonth=Button(self,text="<<Prev",pady=3,command=self.prevMonthAdj)
        prevMonth.grid(row=0,column=0)

        nowTime=Label(self,text=time,font=("tahoma","10","bold"))
        nowTime.configure(foreground="red")
        nowTime.grid(row=0,column=3)

        nextMonth=Button(self,text="Next>>",pady=3,command=self.nextMonthAdj)
        nextMonth.grid(row=0,column=6)

    def createWidgets(self,wkday,numday):
        days=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        pickedDays=[]

        for day in range(7):
            label=Label(self,text=days[day],width=8,font=("tahoma","8","bold"))
            label.grid(row=1,column=day)

        weekday,numDays=monthrange(wkday,numday)
        week=2

        for day in range(1,numDays+1):
            label=Label(self,text=str(day),width=8)
            label.grid(row=week,column=weekday)

            #-------Uncomment Below Section For Button-like View Of The Calendar-------#
            #button=Button(self,text=str(day),width=8)
            #button["command"]=lambda b=button: b.configure(bg="green")
            #button.grid(row=week,column=weekday)
            #--------------------------------------------------------------------------#

            weekday+=1

            if weekday>6:
                week+=1
                weekday=0

    def clrScreen(self):
        for child in self.winfo_children():
            child.destroy()

    def prevMonthAdj(self):
        if self.month-1>0:
            self.month=self.month-1
            self.time=self.monthList[self.month-1]

        else:
            self.year=self.year-1
            self.month=13-self.month
            self.time=self.monthList[self.month-1]

        self.clrScreen()
        self.createWidgets(self.year,self.month)
        self.createHeader(str(self.year)+" "+self.time)

    def nextMonthAdj(self):
        if self.month+1<13:
            self.month=self.month+1
            self.tie=self.monthList[self.month-1]

        else:
            self.year=self.year+1
            self.month=13-self.month
            self.time=self.monthList[self.month-1]

        self.clrScreen()
        self.createWidgets(self.year,self.month)
        self.createHeader(str(self.year)+" "+self.time)

class infoPanel(LabelFrame):
    def __init__(self,master,staffName,staff):
        LabelFrame.__init__(self,master,text=staffName,font=("tahoma","12","bold"),pady=10)
        self.grid(row=1,column=0)
        self.createWidgets(staff)

    def createWidgets(self,staff):
        def getDays():
            updateScreen()
            currentRequestedDays=list(filter(None,set(reqList.get("1.0",END+" -1c").strip().split("\n"))))
            currentRequestedDays.sort()

            if validateDate(currentRequestedDays):
                requestDays=[]
                requestDays=list(set(staff.requestDays+currentRequestedDays))
                requestDays.sort()

                database=shelve.open("staffDB",writeback=True)

                if len(requestDays) > int(database[staff.userName].Left) and txtVar["Left"].get() <= int(database[staff.userName].Left):
                    messagebox.showwarning("Warning", "Insufficient Days Left")

                else:
                    if messagebox.askyesno("Warning", "Sending As Non-Urgent(2 weeks ahead)?"):
                        if checkDays(currentRequestedDays):
                            database[staff.userName].requestDays=requestDays
                            requestStatus.set("Request Sent -{} days(s) in total.".format(len(currentRequestedDays)))

                        else:
                            messagebox.showerror("Warning","Your Request Must Be at least 2 Weeks In Advance")

                    else:
                        database[staff.userName].requestDays=requestDays
                        requestStatus.set("Request Sent - {} days(s) in total.".format(len(currentRequestedDays)))

                    database.close()

                dateClear()

            else:
                messagebox.showerror("Warning","Wrong Date Format!")

        def checkDays(requestDates):
            firstYear, firstMonth, firstDay=re.compile(r'(\d\d\d\d)(\d\d)(\d\d)').search(requestDates[0]).groups()
            return datetime(int(firstYear),int(firstMonth),int(firstDay)) - timedelta(days=14) > datetime.now()

        def dateClear():
            reqList.delete("1.0",END)

        def validateDate(dayList):
            for date in dayList:
                try:
                    datetime.strptime(date,"%Y%m%d %a")

                except:
                    return False

            return True

        def updateScreen():
            db=shelve.open("staffDB")

            for label in ["CarryOver","Entitlement","Taken","Left"]:
                txtVar[label].set(getattr(db[staff.userName],label))

            db.close()

        def viewHistory():
            updateScreen()

            database=shelve.open("staffDB",writeback=True)

            if len(database[staff.userName].rejectDays) > 0:
                warnMsg="Previous Request Was Rejected:\n\n"

                for day in database[staff.userName].rejectDays:
                    warnMsg=warnMsg+day+"\n"

                messagebox.showwarning("Warning",warnMsg)

            newWindow=Toplevel(self)
            newWindow.title("Vacation Request History")
            newWindow.transient(self)

            historyFrame=LabelFrame(newWindow)
            historyFrame.grid(row=0,column=0)

            pendingLabel=Label(historyFrame,text="Pending Requests:",font=("tahoma","8","bold"),pady=6)
            pendingLabel.grid(row=1,column=0)
            pendingLabel.config(foreground="red")

            approvedLabel=Label(historyFrame,text="Approved Requests:",font=("tahoma","8","bold"),pady=6)
            approvedLabel.grid(row=1,column=1)
            approvedLabel.config(foreground="red")

            pendingList=scrolledtext.ScrolledText(historyFrame,width=20,pady=6,wrap=WORD,state="disabled")
            pendingList.grid(row=2,column=0)

            approvedList=scrolledtext.ScrolledText(historyFrame, width=20,pady=6,wrap=WORD,state="disabled")
            approvedList.grid(row=2,column=1)

            plist=database[staff.userName].requestDays
            alist=database[staff.userName].approvedDays

            database[staff.userName].rejectDays=[]
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

        labels={}
        txtVar={}
        rowID=2
        colID=0

        detailFrame=Frame(self)
        detailFrame.grid(row=1,column=0)

        for label in ["CarryOver","Entitlement","Taken","Left"]:
            Label(detailFrame,width=10,pady=6,text=label,anchor="e",font=("tahoma","10")).grid(row=rowID,column=colID,sticky="e")

            colID+=1
            txtVar[label]=IntVar()
            txtVar[label].set(getattr(staff,label))
            labels[label]=Label(detailFrame,textvariable=txtVar[label],width=4,font=("tahoma","10"))
            labels[label].grid(row=rowID,column=colID)
            labels[label].config(foreground="blue")

            colID+=1

            Label(detailFrame,width=6,text="day(s)",font=("tahoma","10")).grid(row=rowID,column=colID)
            rowID+=1

            colID=0

        updateFrame1=Frame(detailFrame,pady=10)
        updateFrame1.grid(row=9,column=0,columnspan=3)

        updateBttn=Button(updateFrame1,text="Refresh Info",font=("tahoma","8","bold"),pady=6,command=updateScreen)
        updateBttn.grid(row=0,column=0)

        updateFrame2=Frame(detailFrame,pady=10)
        updateFrame2.grid(row=10,column=0,columnspan=3)

        historyBttn=Button(updateFrame2,text="View Status",font=("tahoma","8","bold"),pady=6,command=viewHistory)
        historyBttn.grid(row=0,column=0)

        infoFrame=Frame(self)
        infoFrame.grid(row=1,column=1,rowspan=2)

        instruction=Label(infoFrame,text="Enter the vacation dates on each line\ne.g. 20170126 Thu",pady=6)
        instruction.grid(row=0,column=0,columnspan=2)
        instruction.configure(fg="red")

        submitButton=Button(infoFrame,text="Submit",font=("tahoma","8","bold"),width=8,command=getDays)
        submitButton.grid(row=2,column=0)

        clrButton=Button(infoFrame,text="Clear",font=("tahoma","8","bold"),width=8,command=dateClear)
        clrButton.grid(row=2,column=1)

        reqList=scrolledtext.ScrolledText(infoFrame,width=30,wrap=WORD)
        reqList.grid(row=1,column=0,columnspan=2)
        reqList.bind("<1>",lambda event: reqList.focus_set())

        requestStatus=StringVar()
        statusLabel=Label(infoFrame,textvariable=requestStatus,font=("tahoma","10"),pady=6)
        statusLabel.grid(row=3,column=0,columnspan=2)
        statusLabel.config(fg="blue")
