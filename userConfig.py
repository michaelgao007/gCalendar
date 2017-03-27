#!/usr/bin/env python3

import shelve

class employee():
    def __init__(self,userName,passWord,firstName,lastName,CarryOver,Entitlement,Taken,supervisor,requestDays=[],approvedDays=[],rejectDays=[]):
        self.userName=userName
        self.passWord=passWord
        self.firstName=firstName
        self.lastName=lastName
        self.CarryOver=CarryOver
        self.Entitlement=Entitlement
        self.requestDays=requestDays
        self.Taken=Taken
        self.Left=self.CarryOver+self.Entitlement-self.Taken
        self.supervisor=supervisor
        self.approvedDays=approvedDays
        self.rejectDays=[]

if __name__=='__main__':

#-------------Initialize Employees Information-------------#

    ygao=employee("ygao","001001","Yifeng","Gao",2,10,0,"Jason Sheldon")
    jsheldon=employee("jsheldon","tango1","Jason","Sheldon",3,12,0,"Jason Sheldon")
    ecarballo=employee("ecarballo","dd002001","Erik","Carballo",2,15,0,"Jason Sheldon")

#-------------End Of Initialize Employees Information-------------#

    empList=[]
    empList.append(ygao)
    empList.append(jsheldon)
    empList.append(ecarballo)

#-------------Save Employee Inital Information To Database-------------#

    database=shelve.open("staffDB")

    for staff in empList:
        database[staff.userName]=staff

    database.close()

#-------------Endo Of Save Employee Inital Information To Database-------------#
