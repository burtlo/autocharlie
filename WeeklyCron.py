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
    
# EVEN later
-----------

*use checksum to compare weekly schedule in original format, as received, to
    be able to detect more minor changes in show name, etc. that *may* warrant 
    changes to website
    
"""
#import SpinPapiClient as Papi

import SpinPapiLib as SPLib
import time
import local




def sched2charlieSched (sched):
    '''
    accepts a demetafied sched
    strip out Rivendellshows
    current decision: don't do day adjustment for shows before 6am in this 
        function
    returns a charlieSched, containing minimal info needed to run cron job
    '''
    print 'sched2charlieSched()'
    print
    charlieSched = {}
    x = 0
    for day in sched:
        print 'day in sched -> ', str(day)
        charlieSched [day] = {}
        for show in sched[day]:
            # key is concat of OffairTime & OnairTime
                # this avoids duplicate records when two shows occupy identical
                # time slots during the same day
            x += 1
            print 'type(show) -> ', str(type(show))
            print 'show -> ', str(show)
            print "show['OffairTime'] -> ", str(show['OffairTime']), str(type(show['OffairTime']))
            key = x
            #key = ''.join([ show['OffairTime'], show['OnairTime'] ])
            charlieSched[day][key]['OffairTime'] = show['OffairTime']
            charlieSched[day][key]['OnairTime']  = show['OnairTime']
    return charlieSched

#MAIN========================

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
                        
 
#load fresh copy of weekly schedule via spinitron API                       
fullSched = SPLib.FreshPapi1()

print 'fullSched'
print 'type(fullSched) -> ', str(type(fullSched))
print fullSched

'''
schedKeys = fullSched.keys()
print schedKeys
'''

'''
#convert spinitron Schedule to CharlieSched (very stripped down)
charlieSched = sched2charlieSched(fullSched)

#create datestamp filename
saveName = 'CharlieSched-' + time.strftime("%Y-%m-%d:%H:%M") + '.pkl'

#save pickle (for future use by HourlyCron.py)
SPLib.PickleDump(saveName, charlieSched, local.charlieSchedPath)
'''
