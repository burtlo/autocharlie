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

#@contextmanager
def stdout_redirector(stream):
    '''
    see:
        http://eli.thegreenplace.net/2015/redirecting-all-kinds-of-stdout-in-python/
    example code using stdout_redirector:
        f = io.StringIO()
        with stdout_redirector(f):
            print('foobar')
            print(12)
        print('Got stdout: "{0}"'.format(f.getvalue()))
    '''
    old_stdout = sys.stdout
    sys.stdout = stream
    try:
        yield
    finally:
        sys.stdout = old_stdout


def getCharlieSched():
    '''
    returns newest charlieSched from folder specified in key.charlieSched
    '''
    #save current working dir
    current = os.getcwd()
    charlieSched = SPlib.OpenPickle(SPlib.newestPickle(local.charlieSchedPath), 
                                    local.charlieSchedPath)
    #return to current working dir 
    os.chdir(current)
    return charlieSched
    
def getCurrentTime():
    '''
    returns:
        LastHour(int (0 .. 23))
        fullDayString
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
    
def day2spinDay(fullDayStr, hour):
    '''
    adjust for the fact that Spinitron day starts at 6am instead of midnight
    accepts full day name string
    returns adjusted full day name string
    #TODO: does this need to be implemented in datetime module???
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
    
def spinDay2day(spinDay, hour):
    '''
    converts spinitron day to real day, which only happens between
    midnight and 6am
    accepts:
        spinDay: full string day, with day ending @ 6am
        hour: int (0 .. 23) = this is the hour that the show ends
    returns:
        day string, adjusted back from spinday to realday
    '''
    day2num = {'Monday':0, 'Tuesday':1, 'Wednesday':2, 'Thursday':3,
           'Friday':4, 'Saturday':5, 'Sunday':6}
    num2day = { 7: 'SaturdayAFTER', -1: 'Sunday' , 0 : 'Monday' , 
            1 : 'Tuesday' , 2 :'Wednesday',  3 : 'Thursday' , 
            4 : 'Friday' , 5 :'Saturday', 6 : 'Sunday'}  
    realDayStr = spinDay
    if hour < 7:
        realDayStr = num2day[((day2num[spinDay] + 1) % 7)]
    return realDayStr
    
def spinDay22day(spinDay, time):
    '''
    better spinDay2day
    converts spinitron day to real day, which only happens between
    midnight and 6am
    accepts:
        spinDay: full str day, with day ending @ 6am
        time: in datetime.time format (this is the time the show ends)
    returns:
        *date* in datetime.date format (???)
        perhaps other formats, if it is discovered that these are needed
    '''
    day2num = {'Monday':0, 'Tuesday':1, 'Wednesday':2, 'Thursday':3,
           'Friday':4, 'Saturday':5, 'Sunday':6}
    num2day = { 7: 'SaturdayAFTER', -1: 'Sunday' , 0 : 'Monday' , 
            1 : 'Tuesday' , 2 :'Wednesday',  3 : 'Thursday' , 
            4 : 'Friday' , 5 :'Saturday', 6 : 'Sunday'}  
    cutoff = DT.time(6, 0, 0)
    realDayStr = spinDay
    if not(time > cutoff):
        realDayStr = num2day[((day2num[spinDay] + 1) % 7)]
    return realDayStr        
    
def getShows2Archive (sched, LastHour, spinDay):
    '''
    accepts:
        sched = schedule in CharlieSched format
        LastHour int in range from 0 ..23
        spinDay = full string day name, spinDays end @ 6am
    returns:
        a list of all shows that ended during the last hour,
    '''
    retList = []
        
    for show in sched[spinDay]:
        #print
        #print 'GS2A show -> ',str(show)
        #print 'GS2A sched[day][show] -> ', str(sched[day][show])
        showHour = int(str(sched[spinDay][show]['OffairTime']).split(':')[0]) 
        #showHour = int(str(show['OffairTime']).split(':')[0])
        if showHour == LastHour:
            retList.append(sched[spinDay][show])
    return retList   
    
def strTime2timeObject(strTime):
    '''
    accepts:
        strTime: string in this format: "00:00:00"
    returns:
        datetime.time object (hours, minutes, seconds, no date info)
    '''
    #below code is inefficient.  Oh well
    myHour = int(str(strTime).split(':')[0])
    myMin = int(str(strTime).split(':')[1])
    mySec = int(str(strTime).split(':')[2])
    DTtime = DT.time(myHour, myMin, mySec)
    return DTtime   

def mytime2DT(time, day):
    '''
    all "time math" needs to happen in datetime or dateutil format
    #TODO:
    note: this code doesn't use day string, instead internally implements its 
        own day to spinDay conversion
    accepts: 
        time: string in "00:00:00" format
        day: full string (ex: "Sunday")
    returns:
        time in datetime format
    '''
    myHour = int(str(time).split(':')[0])
    myMinute = int(str(time).split(':')[1])
    mySecond = int(str(time).split(':')[2])
    DTtime = DT.datetime.now() + relativedelta(hour=myHour, minute=myMinute,
         second=mySecond, microsecond=0) 
    nowDay = num2day[DTtime.weekday()]
    print 'nowDay -> ', str(nowDay)
    print 'day -> ', str(day)
    if (nowDay != day):
        DTtime = DTtime - DT.timedelta(days=1)

    return DTtime

def numArchives(start,end):
    '''
    accepts:
        start, end: type = datetime.datetime
    '''
    partialEnd = False
    startHour = start.timetuple().tm_hour
    endHour = end.timetuple().tm_hour
    if start.timetuple().tm_mday != end.timetuple().tm_mday:
        endHour += 24
    numHours = endHour - startHour
    #partialEnd is True if the last archived hour to grab needs to have its 
        # end truncated
        # if show ends in the 59th minute, we consider show to end on the hour
    if end.timetuple().tm_min > 0 and end.timetuple().tm_min < 59:
        numHours +=1
        partialEnd = True
    return numHours, partialEnd
    
def buildChunkList(show, spinDay):
    '''
    accepts:
        show in showsToArchive format
        spinDay: fullStrDay (ex: 'Sunday'), spinDay ends @ 6am
    returns:
        ChunkList (a list of hour long archives that will be used to build
            mp3 archive for a particular show)
        Each element of the ChunkList is a dict containing the following:
            'StartTime' : type = datetime.datetime.timetuple()
            'Delta': type = datetime.timedelta
    '''
    #determine start and end of show, with deltas added in
    startHour = strTime2timeObject(show['OnairTime'])
    print
    print 'spinDay22day(spinDay, startHour) ->',
    print spinDay22day(spinDay, startHour)
    showStart = mytime2DT(show['OnairTime'],spinDay22day(spinDay, 
                          startHour)) + relativedelta(minutes=startDelta)
    endHour = strTime2timeObject(show['OffairTime'])
    showEnd = mytime2DT(show['OffairTime'],spinDay22day(spinDay, 
                          endHour)) + relativedelta(minutes=endDelta)

    print 'showStart -> ', str(showStart)
    print 'showEnd -> ', str(showEnd)
    print type(showEnd)
    print
    
    # if start time > end time, then show must stradle midnight hour
    if showStart > showEnd:
        # I think this will fix matters if a show straddles midnight
        # otherwise, maybe get a 24 hour + audio archive ?!?!
        showStart = showStart + relativedelta(days=-1)
        
    duration = showEnd - showStart
    duraSeconds = duration.seconds
    print 'duraSeconds -> ', duraSeconds

    print 'show duration: -> ', str(duration)
    print 'type(duration) -> ', str(type(duration))
    print 'showStart -> ', str(showStart)
    print 'showEnd -> ', str(showEnd)
    
    showHours, partialEnd = numArchives(showStart, showEnd)
    print showHours #start counting @ zero
    print range(showHours)
    partialOffset = 0
    if partialEnd:
        partialOffset = 1
    
    
    chunkList = []
    chunk= {}
    count = 0
    #if the show is an hour or less, does not stradle an hour, and doesn't end
        # at the end of an hour, this is an edge case ...
    if showHours == 1 and partialEnd == True:
        chunk['StartTime'] = showStart
        chunk['TimeDelta'] = showEnd - showStart
    
    else: #not an edge case
        # offset = time from beginning of show to end of first hour
            # ex: show starts at 2:15, offset is 45 minutes
        offset = (showStart + relativedelta(hours=+1, 
                            minute =0, second=0)) -showStart
          
        if count < showHours:
            chunk['StartTime'] = showStart
            chunk['TimeDelta'] = offset
            chunkList.append(chunk)
            count += 1
        
        while count + partialOffset < showHours: # working with a complete hour
            chunk = {}   
            chunk['StartTime'] = chunkList[-1]['StartTime'] + \
                            chunkList[-1]['TimeDelta']
            chunk['TimeDelta'] = DT.timedelta(seconds=3600)
            chunkList.append(chunk)
            count += 1
        
        if partialEnd:
            chunk = {}
            chunk['StartTime'] = chunkList[-1]['StartTime'] + \
                            chunkList[-1]['TimeDelta']
            chunk['TimeDelta'] = showEnd - chunk['StartTime']
            chunkList.append(chunk)
                                        
    return chunkList

def pad(shortStr, padChar = '0', fullLen = 2):
    '''
    accepts:
        a string 
        padChar (a single character string)
        len (int) desired length of output string
    returns:
        a string with padding prepended
    '''
    padding = ''
    for i in range(fullLen - len(shortStr)):
        padding = ''.join((padding, padChar ))
    retStr = ''.join((padding, shortStr))
    return retStr
        
    
        
def buildmp3(show, spinDay):
    '''
    accepts:
        show in showsToArchive format
        spinDay: fullStrDay (ex: 'Sunday'), spinDay ends @ 6am
    returns:
        an mp3 for archiving
    '''

    #each hour has a start and end time within the hour
        # convert start & end times to datetime format, add in time deltas
        
    #if len(chunkList) == 0:
        #errorNow = DT.datetime.now() + relativedelta(hour=0, minute=0, second=0, microsecond=0)
    #elif len(chunkList) == 1:
        #pick start & end points to create mp3Out
        #for this hour long archive (aka "chunk"), create start and end attributes
    #else (two or more archives to grab):
        #for first archive:
            #modify start attribute
        #for last archive in list:
            #modify end attribute
    pass

def cleanOutFolder(folder, extension=''):
    '''
    remove all files in designated folder (absolute path, please), optionally 
        filtered to files with the specified extension (extension must include 
        leading dot)
    previous working directory is restored 
    return value = list containing filenames of deleted files
    '''
    current = os.getcwd()
    os.chdir(folder)
    rex = ''.join(('*',extension))
    hatchetList = list(glob.iglob(rex))
    for el in hatchetList:
        os.remove(''.join((folder,'/',el)))
    os.chdir(current)
    return hatchetList

def audioConcat(sourceFolder, destFolder, postfix = '.mp3'):
    '''
    concatenate all audio files with the specified postfix
        (audio source files sorted alphabetically)
    copy concatenated audio file into destFolder, name = "New.<postfix>"
    returns 1 on success
    '''
    current = os.getcwd()
    os.chdir(sourceFolder)
    targetFile = ''.join((destFolder,'new',postfix))
    #grab list of files in sourceFolder
    rex = ''.join(('*',postfix))
    concatList = sorted(list(glob.iglob(rex)))
    #if there are multiple audio files in the folder where we expect them ..
    if len(concatList) > 1:
        #then build sox command
        cmd = concatList
        cmd.insert(0,'sox')
        cmd.append(targetFile)
        print '+++++++++++++++++++++++++++++++++++++'
        print 'audioConcat line 412'
        print cmd
        print '+++++++++++++++++++++++++++++++++++++'
        #execute sox command to concat audio files
        call(cmd)
    #else, if there is only one audio file, rename it and move it
    elif len(concatList) == 1:
        sourceFile = ''.join((sourceFolder,concatList[0]))
        os.rename(sourceAudio, targetFile)
    else: # no audio files in folder
        print 'ERROR: no audio files in ',sourceFolder, ' to concat'
    #return to current working dir 
    os.chdir(current)
    print 'END: audioConcat'

def createAudioChunks(chunkList, tmpFolder):
    '''
    using chunkList, populate tmpFolder with mp3 chunks for subsequent
    concatenation.
    mp3s named 0.mp3, 1.mp3, ...
    no return value ...
    '''
    hatchetList = cleanOutFolder(tmpFolder,'.mp3')
    if len(hatchetList):
        print 'removed -> ', str(hatchetList), ' from ', tmpFolder
    else:
        print tmpFolder, ' started empty.'
    for x, chunk in enumerate(chunkList):
        print 'chunk #' + str(x)
        year = str(chunk['StartTime'].timetuple().tm_year)
        month = pad(str(chunk['StartTime'].timetuple().tm_mon))
        day = pad(str(chunk['StartTime'].timetuple().tm_mday))
        hour = pad(str(chunk['StartTime'].timetuple().tm_hour))
        minute = pad(str(chunk['StartTime'].timetuple().tm_min))
        SourceOgg = ''.join((local.archiveSource, year, '/', month, '/',
                               day, '/', hour, '-00-00.ogg'))
        #fullHour is a boolean
        DeltaSeconds = chunk['TimeDelta'].total_seconds()
        fullHour = (3540 < DeltaSeconds < 3660 )        
        targetMp3 = ''.join((tmpFolder, '/', str(x), '.mp3'))
        if fullHour: # no trim necesary, just convert to mp3
            print tab,'fullHour [',str(x),']'
            print tab,'    ','SourceOgg -> ', str(SourceOgg)
            print tab,'    ', 'targetMp3 -> ', str(targetMp3)
            cmd = ['sox', SourceOgg, targetMp3]
            print cmd
            call(cmd)
        else: #trim the hour long archive down to size
            startTrim = str(60 * int(minute))
            print tab,'Not fullHour [',str(x),']'
            print tab,'    SourceOgg -> ', str(SourceOgg)
            print tab,'    targetMp3 -> ', str(targetMp3)
            print tab,'    startTrim -> ', str(startTrim)
            print tab,'    DeltaSeconds -> ', str(DeltaSeconds)
            cmd = ['sox', SourceOgg, targetMp3, 'trim', startTrim, str(DeltaSeconds)]
            print cmd
            call(cmd)    
    
    
import os
import local
import key
import SpinPapiLib as SPlib

import datetime as DT
from dateutil.relativedelta import *
import calendar

import pprint

from subprocess import call

from contextlib import contextmanager
import sys

import glob
import ftplib

# example of sox and call usage:
    # http://ymkimit.blogspot.com/2014/07/recording-sound-detecting-silence.html
# option other than subprocess.call -> os.system

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
           
DEBUGGING = False
   

if __name__ == '__main__':
    
    tab = '    '
    pp = pprint.PrettyPrinter(indent=4)
    
    #Now,as defined below, is actually the start of today
    Now = DT.datetime.now() + relativedelta(hour=0, minute=0, second=0, microsecond=0)

    ThisHour = DT.datetime.now() + relativedelta( minute=0, second=0, microsecond=0)
    print '===================================================================='
    print 'HOURLYCRON.py ', str(DT.datetime.now())
    print '===================================================================='    
    #print 'ThisHour -> ', str(ThisHour)
    
    startDelta = local.startDelta
    endDelta = local.endDelta
    
    #grab most recentCharlieSched pickle out of designated folder
    charlieSched = getCharlieSched()
    #print charlieSched
    
    #LastHour is two hours ago if EndDelta is greater than zero
    LastHour, today = getCurrentTime()
    #adjust time to Spinitron time
    spinDay = day2spinDay(today, LastHour)
    print tab, 'LastHour -> ', LastHour
    print tab, 'today -> ', today
    print tab, 'spinDay -> ', spinDay
    
    #======================================
    # make list of shows to archive
    #======================================

    if DEBUGGING:
        #changing LastHour & spinDay hijacks current time
        #showToArchive will be the Euphonic Smorgasbord (as of June 2016)
        LasthHour = 12
        spinDay = 'Friday'
    showsToArchive = getShows2Archive(charlieSched, LastHour, spinDay) 
        
    print '==========================================='
    print 'showsToArchive ->'
    print tab, str(showsToArchive)
    print '=========================================='
    
    # if there's going to be something to archive, then open ftp client
    if len(showsToArchive) > 0:
        ftp = ftplib.FTP(key.host, key.username, key.passwd)
        ftp.cwd(local.remote)
        
    #================================================================
    # build mp3 for each show in list
    #================================================================
    for show in showsToArchive:
        # build list of audio archive chunks to concat
        chunkList = buildChunkList(show, spinDay)
        print "====================="
        print "PrettyPrint chunkList:"
        pp.pprint(chunkList)
        print "====== END: PrettyPrint chunkList ===="
        
        # create correct mp3 for each chunk of show to archive
        createAudioChunks(chunkList, local.tmpMp3)
        print 'AudioChunks created for: ', str(show)

        # sox-concat the audio fles just put into tmpMp3 folder
        audioConcat(local.tmpMp3, local.Mp3Staging)
        #if audioConcat was successful:
        if True: # because success is the only option!
            # send "New.mp3" to correct folder on webserver, using ftp
            timeList = show['OnairTime'].split(':')
            showStart = ''.join((timeList[0],timeList[1]))
            subfolder = ''.join((day2shortDay[spinDay], showStart)) # ex: Sun1300
            remoteTargetFolder = ''.join((local.remote, subfolder))
            ftp.cwd(remoteTargetFolder)
            os.chdir(local.Mp3Staging)
            localMp3 = 'new.mp3'
            myfile = open(localMp3, 'rb')
            ftp.storbinary('STOR' + localMp3 , myfile)
            myfile.close()
            # Using scp, er, ftp, mv "new.mp3" to "current.mp3"
            ftp.rename(localMp3, 'current.mp3') # not really "local" mp3 anymore ...
            
    if len(showsToArchive) > 0:
        ftp.close()        
    print        
    print '++++++++++++++++++++++++++++++++++++++++++++++'
    print 'END of HourlyCron -> ', str(DT.datetime.now() + relativedelta(microsecond=0))
    print '++++++++++++++++++++++++++++++++++++++++++++++'
    print


        
