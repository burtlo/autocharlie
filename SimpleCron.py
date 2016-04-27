# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 20:27:30 2016

@author: lmadeo

#TODO:
    April 26
    Decide where adjustment should be made to deal with timeshifts
        *could be done to original schedule
        *schedule could be adjusted to one long list sorted from 0-168 (modulo)
"""

import SpinPapiClient as Papi
import SpinPapiLib as SPlib
import admin
import key
import local

import myClasses

import datetime as DT
from dateutil.relativedelta import *
import calendar

def getArchivables(sched, LastHour, day):
    '''
    return a list of all shows that ended during the last hour
    LastHour in format 23:00:00
    '''
    retList = []
    syndicated = False
    for show in sched[day]:
        showHour = int(str(show['OffairTime']).split(':')[0])

        if showHour == LastHour:
            for DJ in show['ShowUsers']:
                if DJ['DJName'] == 'Rivendell':
                    syndicated = True
            show['syndicated'] = syndicated
            retList.append(show)
    return retList, syndicated
            
        

#MAIN
#key.py should be obtained locally, not available from repository
client = Papi.SpinPapiClient(key.userid, key.secret)

#num2day has been modified to align with date.weekday() RTFM
num2day = { 7: 'SaturdayAFTER', -1: 'SundayBEFORE' , 0 : 'Monday' , 
            1 : 'Tuesday' , 2 :'Wednesday',  3 : 'Thursday' , 
            4 : 'Friday' , 5 :'Saturday', 6 : 'Sunday'}
                        
                        
if __name__ == '__main__':
    
    CTnow = DT.datetime.now() + relativedelta(hour=0, minute=0, second=0, microsecond=0)    
    charlieTime = myClasses.CurrentTime(CTnow)
    '''
    print "charlieTime"
    print charlieTime
    '''

    
    #load newest schedule
    sched, comment, timeStamp = admin.loadNewestSchedule()
    
    Now = DT.datetime.now() + relativedelta(hour=0, minute=0, second=0, microsecond=0)
    ThisHour = DT.datetime.now() + relativedelta( minute=0, second=0, microsecond=0)
    print ThisHour
    LastHour = ThisHour + relativedelta(hours = -1)
    print LastHour
    print LastHour.weekday()
    today = num2day[LastHour.weekday()]

    timeTuple = str(LastHour).split(':')[0]
    LastHour = int(timeTuple.split(' ')[1])
    print LastHour
    
    showList, syndicated = getArchivables(sched, LastHour, today)
    print syndicated
    for show in showList:
        print show['ShowName']
        print '    '+show['OffairTime']
        print '    '+str(show['syndicated'])
    '''
    TT_LastHour = [ int(i) for i in timeTuple] #cast to ints
    print TT_LastHour
    '''

    
    