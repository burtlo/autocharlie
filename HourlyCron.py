# -*- coding: utf-8 -*-
"""
Created on Wed May 11 15:58:25 2016

@author: lmadeo

hourlyCron.py

#TODO: define CharlieSched format:
    dict of days, keys = fullDayString
        value is a dict
            keys = OffairTime-OnairTime (ex: '08:00:00-06:00:00' )
                OffairTime: 08:00:00
                OnairTime:
example:                
{'Tuesday': {u'08:00:00-06:00:00': 
	{'OffairTime': u'08:00:00', 
	'ShowList': [u'DriftlessMorning'], 
	'Archivable': True, 
	'OnairTime': u'06:00:00'}
     }
}

# FIRST, MOST BASIC ITERATION
-----------------------------

* Grab startDelta and endDelta from local.py

* Open most recent charlieSched in folder specified in local.py

* Build list of shows that ended in last hour
    #note this should be a two hour delay to enable tacking on of endDelta

* For each show in list:
    * build mp3 using pysox
    * send "new.mp3" to correct folder on webserver, using scp
    * Using scp, mv "new.mp3" to "current.mp3"
    
    
# FINE TUMING / FURTHER ITERATION
---------------------------------

* Error checking:
    *target folder exists? If not, create, and log an error
    *local autocharlie folder exists?  If not, create folder, then kick off
        WeeklyCron job
    
* Does loaded charlie sched encompass all 7 days of week?

#TODO: Fix that Chris & Larry show is in ShowList, but not Sonic Landscapes
"""

def getCharlieSched():
    '''
    returns newest charlieSched from key.charlieSched
    '''
    #save current working dir
    current = os.getcwd()
    charlieSched = SPlib.OpenPickle(SPlib.newestPickle(local.charlieSchedPath), 
                                    local.charlieSchedPath)
    #return to current working dir
    os.chdir(current)
    return charlieSched
    
def getTime():
    '''
    returns LastHour(int (0 .. 23)), and fullDayString
    uses relative delta, so 1am minus two hours is 11pm, previous day
    '''
    Now = DT.datetime.now() + relativedelta(hour=0, minute=0, second=0, microsecond=0)
    ThisHour = DT.datetime.now() + relativedelta( minute=0, second=0, microsecond=0)
    print  'GT.ThisHour -> ',str(ThisHour)
    # if end of archive will spill over into next hour, wait an hour before 
    # building archive, otherwise you will be grabbing 60 mon audio archives 
    # that don't exist yet
    if endDelta > 0:
        LastHourRaw = ThisHour + relativedelta(hours = -2)
    else:
        LastHourRaw = ThisHour + relativedelta(hours = -1)        
    print 'GT.LastHourRaw -> ', str(LastHourRaw)
    print 'GT.LastHour.weekday() -> ', str(LastHourRaw.weekday())
    today = num2day[LastHourRaw.weekday()]
    print 'GT.today -> ', str(today)

    timeTuple = str(LastHourRaw).split(':')[0]
    LastHour = int(timeTuple.split(' ')[1])
    #print LastHour
    return LastHour, today
    
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
    
def getShows2Archive (sched, LastHour, day):
    '''
    accepts:
        sched = schedule in CharlieSched format
        LastHour int in range from 0 ..23
        day = full string day name, day adjustment already made
    returns:
        a list of all shows that ended during the last hour,
    '''
    retList = []
        
    for show in sched[day]:
        showHour = int(str(show['OffairTime']).split(':')[0])
        if showHour == LastHour:
            retList.append(show)
    return retList   
    
def buildmp3(show):
    '''
    '''
    #build a list of hour long archives that need to be concatenated
    #if len(archiveList) == 0:
        #error
    #elif len(archiveList) == 1:
        #pick start & end points to create mp3Out
        #for this hour long archive, create start and end attributes
    #else (two or more archives to grab):
        #for first archive:
            #modify start attribute
        #for last archive in list:
            #modify end attribute
    
    
import os
import local
import key
import SpinPapiLib as SPlib

import datetime as DT
from dateutil.relativedelta import *
import calendar

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
    
    Now = DT.datetime.now() + relativedelta(hour=0, minute=0, second=0, microsecond=0)
    ThisHour = DT.datetime.now() + relativedelta( minute=0, second=0, microsecond=0)
    
    startDelta = local.startDelta
    endDelta = local.endDelta
    
    #grab most recentCharlieSched pickle out of designated folder
    charlieSched = getCharlieSched()
    #print charlieSched
    
    #LastHour is two hours ago if EndDelta is greater than zero
    LastHour, today = getTime()
    #adjust time to Spinitron time
    today = dayAdjust(today, LastHour)
    print 'LastHour -> ', LastHour
    print 'today -> ', today
    
    ShowsToArchive = getShows2Archive(charlieSched, LastHour, today)
    
    for show in ShowsToArchive:
        # build mp3 using pysox
        buildmp3(show)
        # send "new.mp3" to correct folder on webserver, using scp
        # Using scp, mv "new.mp3" to "current.mp3"
        

        