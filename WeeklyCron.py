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

import SpinPapiLib as SPLib
import local


def sched2charlieSched (sched):
    '''
    accepts a demetafied sched
    strip out Rivendellshows
    current decision: don't do day adjustment for shows before 6am in this 
        function
    returns a charlieSched, containing minimal info needed to run cron job
    '''
    charlieSched = {}
    for day in sched:
        charlieSched [day] = {}
        for show in sched[day]:
            # key is concat of OffairTime & OnairTime
                # this avoids duplicate records when two shows occupy identical
                # time slots during the same day
            key = ''.join([ show['OffairTime'], show['OnairTime'] ])
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
                        
 
                       
fullSched = SPLib.FreshPapi1()
charlieSched = sched2charlieSched(fullSched)
