# -*- coding: utf-8 -*-
"""
Created on Wed May 11 15:03:20 2016

@author: lmadeo

ftpSetup is largely a copy of WeeklyCron.py

    
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
    return ftp
    
def sched2charlieSched2remoteFolders (sched):
    '''
    accepts:
        demetafied sched
    strips out Rivendellshows
    for each non-Rivendell show, create a folder in /wdrtradio.org/Audio3
        in remote website server, via FTP
    returns:
        charlieSched, containing minimal info needed to run cron job
        *note*: days are spinitron days, that end at 6am, not midnight
    '''
    print 'sched2charlieSched()'
    print
    charlieSched = {}
    # build charlieSched day by day
    for day in sched:
        charlieSched [day] = {}
        for show in sched[day]:
            #NOTE: '-' join is necessay, string will be parsed later
                # by searching for dash
            #NOTE: The key below prevents duplicates, by sorting out shows that
                #start and end at the same time
            key = '-'.join([ day2shortDay[day], show['OnairTime'], show['OffairTime'] ])
            charlieSched[day][key] = {}   
            charlieSched[day][key]['OffairTime'] = show['OffairTime']
            charlieSched[day][key]['OnairTime']  = show['OnairTime']
            try:
                #no ShowList will kick off error
                ShowList = charlieSched[day][key]['ShowList']
            except:
                charlieSched[day][key]['ShowList'] = []
            #now we know that ShowList exists
            charlieSched[day][key]['ShowList'].append(show['ShowName'])
            try:
                # Archivable not set will cause error
                Q = charlieSched[day][key]['Archivable']
                # if archivable is true, give it a chance to turn false
                    # if it's false, it stays false
                if charlieSched[day][key]['Archivable']:
                    charlieSched[day][key] = isArchivable(show)
            except:
                charlieSched[day][key]['Archivable'] = isArchivable(show)
    
    ftp = startFTP()
    # create Audio3 folder, this try/except is unecessary, but it's fun
    try:
        ftp.cwd('/wdrtradio.org/Audio3')
    except ftplib.error_perm:
        print 'no pre-existing Audio3 folder'
        ftp.mkd('/wdrtradio.org/Audio3')
        print 'Audio3 has been created'
        
    tempSched = deepcopy(charlieSched)
    for day in tempSched:
        print day
        for timeslot in tempSched[day]:
            #if timeslot is not archivable, then remove it from charlieSched
            if not(tempSched[day][timeslot]['Archivable']):
                #print '\ts2cs> deleted: ', str(tempSched[day][timeslot]['ShowList'])
                del charlieSched[day][timeslot]
            #for my sneaky purposes, run MyFunc if timeslot is archivable
            else:
                folderName = createRemoteFolder(timeslot)
                print folderName
    return charlieSched

def createRemoteFolder(timeslot):
    '''
    accepts a timeslot string, example format:
        Sun1700 (sunday @ 5pm)
    '''
    tempList = timeslot.split('-') #split timeslot @ dashes ex: 'Sat-20:00:00-22:00:00'
    timeList = tempList[1].split(':') #split start time ex: 15:00:00
    #we assume we're already in Audio3 folder
    destFolder = ''.join((tempList[0],timeList[0], timeList[1]))
    ftp.mkd(destFolder)
    return destFolder
    
    
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
    
    
#MAIN========================
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
                        
 
#load fresh copy of weekly schedule via spinitron API                       
fullSched = SPLib.FreshPapi1()


schedKeys = fullSched.keys()
print 'schedKey -> ', str(schedKeys)

#convert spinitron Schedule to CharlieSched (very stripped down)
charlieSched = sched2charlieSched2remoteFolders(fullSched)

#create datestamp filename
#saveName = 'CharlieSched-' + time.strftime("%Y-%m-%d:%H:%M") + '.pkl'

#save pickle (for future use by HourlyCron.py)
#SPLib.PickleDump(saveName, charlieSched, local.charlieSchedPath)

print '++++++++++++++++++++++++++++++++++++++++++++++'
print 'END: ftpSetup.py'    
print time.asctime()
print '++++++++++++++++++++++++++++++++++++++++++++++'