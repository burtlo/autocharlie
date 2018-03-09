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

#import myClasses
from myClasses import SchedInfo, ShowTempTime, CurrentTime

import datetime as DT
from dateutil.relativedelta import *
import calendar

def showUsersCleanUp(show):
    '''
    strip off info about DJ images 
    and return cleaned up show
    '''
    newShowUsers = []
    for user in show['ShowUsers']:
        if 'DJImgS' in user:
            del user['DJImgS']
        if 'DJImgL' in user:
            del user['DJImgL']
        newShowUsers.append(user)
    show['ShowUsers'] = newShowUsers
    return show
    
def dayAdjust(fullDayStr, hour):
    '''
    adjust for the fact that Spinitron day starts at 6am instead of midnight
    accepts full day name string
    returns adjusted full day name string
    '''
    day2num = {'Monday':0, 'Tuesday':1, 'Wednesday':2, 'Thursday':3,
           'Friday':4, 'Saturday':5, 'Sunday':6}
    num2day = { 7: 'SaturdayAFTER', -1: 'Sunday' , 0 : 'Monday' , 
            1 : 'Tuesday' , 2 :'Wednesday',  3 : 'Thursday' , 
            4 : 'Friday' , 5 :'Saturday', 6 : 'Sunday'}
    if hour < 7:
        yesterday = num2day[((day2num[fullDayStr] - 1) % 7)]
        fullDayStr = yesterday
    return fullDayStr
    
def getArchivables(sched, LastHour, day):
    '''
    accepts:
        sched = demetafied schedule
        LastHour int in range from 0 ..23
        day = full string day name
    returns:
        a list of all shows that ended during the last hour,
        show['Syndicated'] is added to each show
            Syndicated = True if Rivendell is one of the DJs for the show
    
    '''
    retList = []
    syndicated = False
    
    day = dayAdjust(day, LastHour)
        
    for show in sched[day]:
        show = showUsersCleanUp(show)
        # TODO: Is this the point to adjust for 6am start of day?
        showHour = int(str(show['OffairTime']).split(':')[0])

        if showHour == LastHour:
            for DJ in show['ShowUsers']:
                if DJ['DJName'] == 'Rivendell':
                    syndicated = True
            show['Syndicated'] = syndicated
            retList.append(show)
    return retList
            
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
num2day = { 7: 'SaturdayAFTER', -1: 'Sunday' , 0 : 'Monday' , 
            1 : 'Tuesday' , 2 :'Wednesday',  3 : 'Thursday' , 
            4 : 'Friday' , 5 :'Saturday', 6 : 'Sunday'}
            
num2dayShort = { 7: 'SatAFTER', -1: 'SunBEFORE' , 0 : 'Mon' , 
            1 : 'Tue' , 2 :'Wed',  3 : 'Thu' , 
            4 : 'Fri' , 5 :'Sat', 6 : 'Sun'}
            
day2shortDay = { 'Monday' : 'Mon', 'Tuesday' : 'Tue', 
                'Wednesday' : 'Wed', 'Thursday': 'Thu', 'Friday': 'Fri',
                'Saturday': 'Sat', 'Sunday': 'Sun'}
                
day2num = {'Monday':0, 'Tuesday':1, 'Wednesday':2, 'Thursday':3,
           'Friday':4, 'Saturday':5, 'Sunday':6}
                        
                        
if __name__ == '__main__':
    
    tab = '   '
    
    CTnow = DT.datetime.now() + relativedelta(hour=0, minute=0, second=0, microsecond=0)    
    charlieTime = CurrentTime(CTnow)
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
    print 'LastHour -> ', str(LastHour)
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
    print 'Show(s) that ended in the previous hour:'
    showList = getArchivables(sched, LastHour, today)
    for show in showList:
        if show['Syndicated'] == True:
            print tab + show['ShowName']
            print tab + tab +show['OffairTime']
            print tab + tab +str(show['Syndicated'])
    print '-----------------------------------------------'
    '''
    TT_LastHour = [ int(i) for i in timeTuple] #cast to ints
    print TT_LastHour
    '''

    '''
    ###################################################################
    # Iterate through all hours in week and list shows
    # that are syndicated
    ###################################################################
    for weekHour in range(167):
        
        day, hour = convert2dayHour(weekHour)
        dayStr = num2dayShort[day]
        pad = ''
        #print hour
        if hour <= 10:
            pad = '0'
        KlannFolder = ''.join([ dayStr , pad , str(hour) , '00'])
        #print KlannFolder
        showList = getArchivables(sched, hour, num2day[day])
        syn = False
        for show in showList:
            if show['Syndicated'] == True:
                syn = True
        if syn == True:
            print KlannFolder
        for show in showList:
            if show['Syndicated'] == True:
                print tab + show['ShowName']
                print tab + tab +show['OffairTime']
                print tab + tab + str(show['ShowUsers'])
                print tab + tab +str(show['Syndicated'])

    '''
    

    ###################################################################
    # Iterate through all hours in week and list shows
    # that are *NOT* syndicated
    ###################################################################
    for weekHour in range(167):
        
        day, hour = convert2dayHour(weekHour)
        dayStr = num2dayShort[day]
        pad = ''
        #print hour
        if hour <= 10:
            pad = '0'
        KlannFolder = ''.join([ dayStr , pad , str(hour) , '00'])
        #print KlannFolder
        showList = getArchivables(sched, hour, num2day[day])
        syn = True
        for show in showList:
            if show['Syndicated'] == False:
                syn = False
        if syn == False:
            print KlannFolder
            x = len(KlannFolder)
            x = int(KlannFolder[x-4:x-2])
        for show in showList:
            if show['Syndicated'] == False and x < 7:
                print tab + show['ShowName']
                print tab + tab +show['OffairTime']
                print tab + tab + str(show['ShowUsers'])
                print tab + tab +str(show['Syndicated'])    
