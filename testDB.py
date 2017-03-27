#!/usr/bin/env python3

#Test script to verify staff information

import shelve
from userConfig import *

database=shelve.open("staffDB")

for staff in database.keys():
    print("======================== "+database[staff].firstName+" "+database[staff].lastName+" ========================")

    for attr in ["userName","firstName","lastName","CarryOver","Entitlement","Taken","Left","supervisor","requestDays","approvedDays","rejectDays"]:
        print(attr+" => "+str(getattr(database[staff],attr)))

    print("===============================================================\n\n")

database.close()
