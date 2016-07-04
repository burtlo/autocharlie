# -*- coding: utf-8 -*-
"""
Created on Wed May 11 15:03:20 2016

@author: lmadeo

WeeklyCron.py

# FIRST, MOST BASIC INTERATION
------------------------------

* Hit Spinitron API & get weekly schedule
* Strip schedule down to a dict: 
    * stripped down schedule = charlieSched
    * fullDayString : DictOfTimeSlots
    * TimeSlot = { CustomKey : {'OnairTime': 'hh:mm:ss', 'OffairTime : 'hh:mm:ss'} }
* Save stripped schedule to CharlieSched folder, as specified in local.py

# OTHER steps to be taken later:
--------------------------------

* use checksum, or similar technique to detect changes in charlieSched, because
    changes to the "skeleton" of the weekly schedule will require multiple
    modifications to the
    *website
    *new folders created, old folders deleted
    
* Special metafication for partial schedule pickles (or send to test folder?)
    
# EVEN later
-----------

*use checksum to compare weekly schedule in original format, as received, to
    be able to detect more minor changes in show name, etc. that *may* warrant 
    changes to website
    
#TODO:
    fix unicode issues, ex:
    'ShowList': [u' \u201cDRIFTLESS JAZZ\u201d ']
    
"""
#import SpinPapiClient as Papi

import SpinPapiLib as SPLib
import time
import local
import key
from copy import deepcopy

import pprint
from ftplib import FTP


def dudFunc(day):
    '''
    used by shced2charlieSched as a default action of doing nothing
    '''
    pass

def startFTP():
    '''
    '''
    ftp = FTP(key.host, key.username, key.passwd)
    
def sched2charlieSched (sched, myFunc = dudFunc):
    '''
    accepts:
        demetafied sched
    strips out Rivendellshows
    current decision: don't do day adjustment for spinitron time
    returns:
        charlieSched, containing minimal info needed to run cron job
        *note*: days are spinitron days, that end at 6am, not midnight
    '''
    print 'sched2charlieSched()'
    print
    charlieSched = {}
    #for day in sched:
    for day in ['Monday']: #comment out this line when testing is done
        #print 'day in sched -> ', str(day)
        charlieSched [day] = {}
        for show in sched[day]:
            #print 'type(show) -> ', str(type(show))
            #print 'show -> ', str(show)
            #print "show['OffairTime'] -> ", str(show['OffairTime']), str(type(show['OffairTime']))
            #NOTE: '-' join is necessay, string will be parsed later
                # by searching for dash
            #NOTE: The key below prevents duplicates, by sorting out shows that
                #start and end at the same time
            key = '-'.join([ day2shortDay[day], show['OnairTime'], show['OffairTime'] ])
            charlieSched[day][key] = {}   
            charlieSched[day][key]['OffairTime'] = show['OffairTime']
            charlieSched[day][key]['OnairTime']  = show['OnairTime']
            try:
                #no ShowList will kick off execpt code
                ErrorCheck = charlieSched[day][key]['ShowList']
            except:
                charlieSched[day][key]['ShowList'] = []
            #now we know that ShowList exists
            charlieSched[day][key]['ShowList'].append(show['ShowName'])
            print str(len(charlieSched[day][key]['ShowList'])), str(charlieSched[day][key]['ShowList'])
            print '\t',str(charlieSched[day][key])
            try:
                # no Archivable will trigger execute except code
                ErrorCheck2 = charlieSched[day][key]['Archivable']
                # if archivable is true, give it a chance to turn false
                    # if it's false, it stays false
                if charlieSched[day][key]['Archivable']:
                    charlieSched[day][key] = isArchivable(show)
            except:
                charlieSched[day][key]['Archivable'] = isArchivable(show)
    tempSched = deepcopy(charlieSched)
    for day in tempSched:
        print day
        for timeslot in tempSched[day]:
            #if timeslot is not archivable, then remove it from charlieSched
            if not(tempSched[day][timeslot]['Archivable']):
                print 'ts2cs> deleted: ', str(tempSched[day][timeslot]['ShowList'])
                del charlieSched[day][timeslot]
            #for my sneaky purposes, run MyFunc if timeslot is archivable
            else:
                print 'ts2cs> archivable: ', str(tempSched[day][timeslot]['ShowList'])
                myFunc(timeslot)
    return charlieSched

def createRemoteFolder(timeslot):
    '''
    #THIS FUNCTION IS CURRENTLY NOT USED#
    supposed to be output:
        ex: Sun0800 <- start of Mr. Koppa's sunday morning neighborhood
    '''
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(timeslot)  
    tempList = timeslot.split('-') #split timeslot @ dashes ex: 'Sat-20:00:00-22:00:00'
    timeList = tempList[1].split(':') #split start time ex: 15:00:00
    destFolder = ''.join((tempList[0],timeList[0], timeList[1]))
    print targetStr
    
def dayAdjust(fullDayStr, hour):
    '''
    #
    #might not  be needed in WeeklyCron context
    #
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
    
def isArchivable(show):
    '''
    accepts:
        show, with full complement of attributes
    returns True if none of the show DJs are Rivendell
    '''
    for DJ in show['ShowUsers']:
        if DJ['DJName'] == 'Rivendell':
            return False
    return True

#==================================MAIN========================    

if __name__ == '__main__':
    
    print '=============================================='
    print 'WeeklyCron.py'    
    print time.asctime()
    print '=============================================='
    #client = Papi.SpinPapiClient(key.userid, key.secret)
    
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
                            
    print 'fullSched' 
    #load fresh copy of weekly schedule via spinitron API                       
    fullSched = SPLib.FreshPapi1()
    
    #print 'fullSched'
    #print 'type(fullSched) -> ', str(type(fullSched))
    #print fullSched
    
    schedKeys = fullSched.keys()
    print 'schedKey -> ', str(schedKeys)
    
    #convert spinitron Schedule to CharlieSched (very stripped down)
    charlieSched = sched2charlieSched(fullSched, dudFunc)
    
    #create datestamp filename
    saveName = 'CharlieSched-' + time.strftime("%Y-%m-%d:%H:%M") + '.pkl'
    
    #save pickle (for future use by HourlyCron.py)
    #TODO: Following line is commented out for testing purposes
    #SPLib.PickleDump(saveName, charlieSched, local.charlieSchedPath)
    
    print '++++++++++++++++++++++++++++++++++++++++++++++'
    print 'END: WeeklyCron.py'    
    print time.asctime()
    print '++++++++++++++++++++++++++++++++++++++++++++++'