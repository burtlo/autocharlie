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
    accepts:
        sched = demetafied schedule
        LastHour in format 23:00:00
        day = full string day name
    returns:
        a list of all shows that ended during the last hour
    
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
            
def sched2charlieSched (sched):
    '''
    accepts a demetafied sched
    strip out Rivendellshows
    returns a charlieSched, containing minimal info needed to run cron job
    '''
    #create charlieSched
    charlieSched = {}
    #for each day in sched:
        #for each show in sched:
            #determine adjusted day
            #maybe I shouldn't implement adjusted day, to stay in line with
                #spinitron and existing folder naming
            #select desired dict elements from show
                #starttime
                #endtime
            #save the desired subset show to charlieSched
            #save 
    pass

def convert2dayHour(weekHour):
    '''
    accept integer range (0 .. 167)
    returns:
        day (range 0 .. 6)
        hour (range 0 .. 23)
    '''
    day = weekHour // 24
    hour = weekHour - (24 * day)
    return day, hour
    
def convert2weekHour(day, hour):
    '''
    accepts:
        day (range 0 .. 6)
        hour (range 0 .. 23)
    returns: integer range (0 .. 167)
    '''
    weekHour = day * 24 + hour
    return weekHour
    
#MAIN
#key.py should be obtained locally, not available from repository
client = Papi.SpinPapiClient(key.userid, key.secret)

#num2day has been modified to align with date.weekday() RTFM
num2day = { 7: 'SaturdayAFTER', -1: 'SundayBEFORE' , 0 : 'Monday' , 
            1 : 'Tuesday' , 2 :'Wednesday',  3 : 'Thursday' , 
            4 : 'Friday' , 5 :'Saturday', 6 : 'Sunday'}
            
num2dayShort = { 7: 'SatAFTER', -1: 'SunBEFORE' , 0 : 'Mon' , 
            1 : 'Tue' , 2 :'Wed',  3 : 'Thu' , 
            4 : 'Fri' , 5 :'Sat', 6 : 'Sun'}
                        
                        
if __name__ == '__main__':
    
    tab = '   '
    
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
    print today

    timeTuple = str(LastHour).split(':')[0]
    LastHour = int(timeTuple.split(' ')[1])
    print LastHour
    
    ############################################################
    # List a show that ended in the last hour, 
    # syndicated = Rivendell is the DJ
    ############################################################
    
    showList, syndicated = getArchivables(sched, LastHour, today)
    print syndicated
    for show in showList:
        print tab + show['ShowName']
        print tab + tab +show['OffairTime']
        print tab + tab +str(show['syndicated'])
    '''
    TT_LastHour = [ int(i) for i in timeTuple] #cast to ints
    print TT_LastHour
    '''

    ###################################################################
    # Iterate through all hours in week and list shows
    ###################################################################
    for weekHour in range(167):
        
        day, hour = convert2dayHour(weekHour)
        dayStr = num2dayShort[day]
        pad = ''
        print hour
        if hour <= 10:
            pad = '0'
        print dayStr + pad + str(hour) + '00'
        showList, syndicated = getArchivables(sched, hour, num2day[day])
        for show in showList:
            print tab + show['ShowName']
            print tab + tab +show['OffairTime']
            print tab + tab +str(show['syndicated'])

    