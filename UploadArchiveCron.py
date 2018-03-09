# -*- coding: utf-8 -*-
"""
Created on Wed May 11 15:58:25 2016

@author: lmadeo

UploadArchiveCron.py

###############################
warning:
This might break if a show spans the end of the spinitron day
In other words, this program assumes that the start and end of a radio show 
    happen during the same day
A good start on fixing this would be to disambiguate the following:
    spinday of HourlyCron execution time
    spinday of show start
    spinday of show end
##############################

CharlieSched format:
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
    * build mp3 using direct call to sox
    * send "new.mp3" to correct folder on webserver, using scp or ftp
    * Using scp or ftp, mv "new.mp3" to "current.mp3"
    
    
# FINE TUNING / FURTHER ITERATION
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
    accepts:
        no inputs, grabs current time from datetime module
    returns:
        LastHour(int (0 .. 23))
        fullDayString (ex: 'Sunday')
    uses relative delta, so 1am minus two hours is 11pm, previous day
    '''
    Now = DT.datetime.now() + relativedelta(hour=0, minute=0, second=0, microsecond=0)
    ThisHour = DT.datetime.now() + relativedelta( minute=0, second=0, microsecond=0)
    print  'GT.ThisHour -> ',str(ThisHour)
    # if end of archive will spill over into next hour, wait an hour before 
    # building archive, otherwise you will be grabbing 60 mon audio archives 
    # that don't exist yet
    if endDelta > 0: 
        if endDelta < local.startHourlyCron: # tail end of show ends in time to build archive
            LastHourRaw = ThisHour + relativedelta(hours = -0)
            print 'line 113'
        else: # tail end of show ends AFTER archiver is ready for it
            LastHourRaw = ThisHour + relativedelta(hours = -0)
            print 'line 116'
    else: # no tail added to show archive, so no spill over to next hour 
        LastHourRaw = ThisHour + relativedelta(hours = -1)   
        print 'line 119'
    print 'GT.LastHourRaw -> ', str(LastHourRaw)
    print 'GT.LastHour.weekday() -> ', str(LastHourRaw.weekday())
    today = num2day[LastHourRaw.weekday()]
    print 'GT.today -> ', str(today)

    timeTuple = str(LastHourRaw).split(':')[0]
    LastHour = int(timeTuple.split(' ')[1])
    #print LastHour
    return LastHour, today
    
def day2spinDay(fullDayStr, hour, startSpinDay):
    '''
    adjust for the fact that Spinitron day starts at 6am instead of midnight
    accepts:
        full day name string (ex: 'Sunday')
        hour: integer in range [0 .. 23]
        startSpinDay: integer in range [0 .. 23]
    
    returns adjusted full day name string
    #TODO: does this need to be implemented in datetime module???
    '''
    day2num = {'Monday':0, 'Tuesday':1, 'Wednesday':2, 'Thursday':3,
           'Friday':4, 'Saturday':5, 'Sunday':6}
    num2day = { 7: 'SaturdayAFTER', -1: 'Sunday' , 0 : 'Monday' , 
            1 : 'Tuesday' , 2 :'Wednesday',  3 : 'Thursday' , 
            4 : 'Friday' , 5 :'Saturday', 6 : 'Sunday'}
    if startSpinDay != 0:
        if hour <= startSpinDay:
            yesterday = num2day[((day2num[fullDayStr] - 1) % 7)]
            fullDayStr = yesterday
    return fullDayStr
    
def spinDay2day(spinDay, hour, startSpinDay):
    '''
    converts spinitron day to real day, which only happens between
    midnight and start of broadcast day (often 6am or midnight)
    accepts:
        spinDay: full string day, ex: "Sunday"
        hour: int [0 .. 23] = this is the hour that the show ends
            #commnt to self: could be beginning or end hour of show, anyway ...
        startSpinDay: int range [0..23] represents the hour that radio broadcast
            day starts, typically either 6am or midnight
    returns:
        day string, adjusted back from spinday to realday
    '''
    day2num = {'Monday':0, 'Tuesday':1, 'Wednesday':2, 'Thursday':3,
           'Friday':4, 'Saturday':5, 'Sunday':6}
    num2day = { 7: 'SaturdayAFTER', -1: 'Sunday' , 0 : 'Monday' , 
            1 : 'Tuesday' , 2 :'Wednesday',  3 : 'Thursday' , 
            4 : 'Friday' , 5 :'Saturday', 6 : 'Sunday'}  
    realDayStr = spinDay
    if startSpinDay != 0:
        if hour <= startSpinDay:
            realDayStr = num2day[((day2num[spinDay] + 1) % 7)]
    return realDayStr
    
def spinDay22day(spinDay, time, startSpinDay):
    '''
    better spinDay2day
    converts spinitron day to real day, which only happens between
    midnight and start of broadcast day (typically midnight or 6am)
    accepts:
        spinDay: full str day, with day ending @ 6am
        time: in datetime.time format (this is the time the show ends)
        startSpinDay = int in range [0..23] ex 6 = 6:00am
    returns:
        realDayStr = a full day string (ex: 'Sunday')
        **NOT* *date* in datetime.date format
        perhaps other formats, if it is discovered that these are needed
    '''
    day2num = {'Monday':0, 'Tuesday':1, 'Wednesday':2, 'Thursday':3,
           'Friday':4, 'Saturday':5, 'Sunday':6}
    num2day = { 7: 'SaturdayAFTER', -1: 'Sunday' , 0 : 'Monday' , 
            1 : 'Tuesday' , 2 :'Wednesday',  3 : 'Thursday' , 
            4 : 'Friday' , 5 :'Saturday', 6 : 'Sunday'}  
    cutoff = DT.time(startSpinDay, 0, 0)
    realDayStr = spinDay
    if not(time >= cutoff):
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
    #I don't think this is getting used now, I'm not really using DT.time class
        anywhere else in the code base, see mytime2DT, below, which is very
        similar to this function, but uses the DT.datetime class
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

def mytime2DT(time):
    '''
    accepts: 
        time: string in "00:00:00" format
        spinDay: full string (ex: "Sunday")
    returns:
        time in datetime format
    '''
    
    myHour = int(str(time).split(':')[0])
    myMinute = int(str(time).split(':')[1])
    mySecond = int(str(time).split(':')[2])
    DTtime = DT.datetime.now() + relativedelta(hour=myHour, minute=myMinute,
         second=mySecond, microsecond=0) 

    #nowDay = num2day[DTtime.weekday()]
    now = DT.datetime.now()
    # assuming that shows are archived less than 24 hours after they are
    # broadcast, now < DTtime only if "time" occured yesterday
    if now < DTtime: 
        DTtime = DTtime - DT.timedelta(days=1)
    return DTtime

def numArchives(start,end):
    '''
    accepts:
        start, end: type = datetime.datetime
    returns:
        numHours: int representing number of hour archive chunks inbetween
            start and end time
        partialEnd: boolean - true if the last archived hour to grab needs to
            have its end truncated.  If show ends in the 59th minute, we consider 
            the show to end on the hour
    '''
    partialEnd = False
    startHour = start.timetuple().tm_hour
    endHour = end.timetuple().tm_hour
    if start.timetuple().tm_mday != end.timetuple().tm_mday:
        endHour += 24
    numHours = endHour - startHour
    if end.timetuple().tm_min > 0 and end.timetuple().tm_min < 59:
        numHours +=1
        partialEnd = True
    return numHours, partialEnd
    

        
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

  
def addNewRemoteFolders(charlieSched):
    '''
    accepts:
        schedule in charlieSched format
    action:
        if a necessary folder on the website doesn't exist, create it
    returns:
        nothing
    '''
    def createRemoteFolder(timeslot):
        '''
        accepts a timeslot string, example format:
           "Sat-20:00:00-22:00:00" = show starts Saturday @ 8pm 
        makes folder as follows:
           "Sat2000" (but only if it doesn't already exist)
        returns:
            name of folder (whether or not it already exists)
        '''
        tempList = timeslot.split('-') #split timeslot @ dashes ex: 'Sat-20:00:00-22:00:00'
        timeList = tempList[1].split(':') #split start time ex: 15:00:00
        subFolder = ''.join((tempList[0],timeList[0], timeList[1]))
        destFolder =  ''.join((local.archiveDest, subFolder))
        try: #make remote audio archive folder if it hasn't been created yet
            sftp.mkdir(destFolder)
            print "NEW AUDIO ARCHIVE FOLDER CREATED -> ",destFolder
        except IOError:
            # folder has already been created, nothing to do
            pass
        return destFolder
    
    #ftp = ftplib.FTP(key.host, key.username, key.passwd)
    sftp = pysftp.Connection(host=key.host, username=key.username, password=key.passwd)
    for day in charlieSched:
        for timeslot in charlieSched[day]:
             createRemoteFolder(timeslot)

def buildChunkList (DTstart, DTend):
    '''
    accepts:
        DTstart, DTend: datetime object
            start and end time of a broadcast that we wish to archive
    returns:
        chunkList (a list of hour long archives that will be used to build
            mp3 archive for a particular show)
        Each element of the ChunkList is a dict containing the following:
            'StartTime' : type = datetime.datetime.timetuple()
                (could start anytime during a clock hour)
            'Delta': type = datetime.timedelta
                (time duration of chunk, start time + delta can't spill over
                 into next clock hour)
         success: boolean
    '''
    chunkList = []
    
    duration = DTend - DTstart
    
    fourHours = DT.timedelta(seconds=60*60*4)
    if DTstart >= DTend or duration > fourHours: #start should be *before* the end!
        success = False
        return chunkList, success
    else:
        duraSeconds = duration.seconds
        
        showHours, partialEnd = numArchives(DTstart, DTend)
        partialOffset = 0
        if partialEnd:
            partialOffset = 1
        
        chunk= {}
        count = 0
        #if the show is an hour or less, does not stradle an hour, and doesn't end
            # at the end of an hour, this is an edge case ...
        if showHours == 1 and partialEnd == True:
            chunk['StartTime'] = DTstart
            chunk['TimeDelta'] = DTend - DTstart
            chunkList.append(chunk)
        
        else: #not an edge case
            # offset = time from beginning of show to end of first hour
                # ex: show starts at 2:15, offset is 45 minutes
            offset = (DTstart + relativedelta(hours=+1, 
                                minute =0, second=0)) -DTstart
              
            if count < showHours:
                chunk['StartTime'] = DTstart
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
                chunk['TimeDelta'] = DTend - chunk['StartTime']
                chunkList.append(chunk)
        
        success = True                                    
        return chunkList,success   

def uniqueSubfolder(folder):
    '''
    accepts:
        folder: string representation of a folder path
    first attempted subfolder to create:
        "0", then "1", etc. until success!!!
    returns: 
        folder: str which represents the whole file path to a new
            subfolder ('folder' + 'newSubFolder')
    '''
    # ensure that there is a trailing backslash on path name
    if folder[-1] != '/':
        folder = "".join((folder, '/'))
    success = False
    count = 0
    current = os.getcwd()
    os.chdir(folder)
    while not success:
        try:
            os.mkdir(str(count))
            success = True
        except:
            count += 1
    print 'old folder -> ',folder       
    folder = "".join((folder, str(count), '/'))
    print 'new folder -> ',folder
    os.chdir(current)
    return folder # it's funny that this is the only exit for this function
                # but it's not at the end ...
  

def pad(shortStr, padChar = '0', fullLen = 2):
    '''
    accepts:
        a string 
        padChar (a single character string)
        len (int) desired length of output string
    returns:
        a string with padding prepended
    typical use: accept '9' and return '09'
    '''
    padding = ''
    for i in range(fullLen - len(shortStr)):
        padding = ''.join((padding, padChar ))
    retStr = ''.join((padding, shortStr))
    return retStr
            
def createAudioChunks (chunkList):
    '''
    accepts:
        ChunkList, as returned by buildChunkList
    Creates: 
        targetFolder which is a unique subfolder of tempAudioFolder
    Populates: 
        targetFolder with alphanumerically sorted mp3 files
        (ex: 0.mp3, 1.mp3, 2.mp3)
    returns:
        targetFolder path as string, targetFolder contains audioChunk mp3s
    '''
   
    #make tempAudioFolder if it doesn't already exist
    os.chdir(local.path)
    tempAudioFolder = "".join((local.path,'tempAudio'))
    try:
        os.chdir(tempAudioFolder)
    except: # TODO: what is the error that above line would raise
        os.mkdir(tempAudioFolder)
    targetFolder = uniqueSubfolder(tempAudioFolder)
    
    
    for x, chunk in enumerate(chunkList):
        #pull info out of a chunk in the chunk list
        print 'chunk #' + str(x)
        year = str(chunk['StartTime'].timetuple().tm_year)
        month = pad(str(chunk['StartTime'].timetuple().tm_mon))
        day = pad(str(chunk['StartTime'].timetuple().tm_mday))
        hour = pad(str(chunk['StartTime'].timetuple().tm_hour))
        minute = pad(str(chunk['StartTime'].timetuple().tm_min))
        SourceOgg = ''.join((local.archiveSource, year, '/', month, '/',
                               day, '/', hour, '-00-00.ogg'))

        DeltaSeconds = chunk['TimeDelta'].total_seconds()
        #fullHour is a boolean
        fullHour = (3540 < DeltaSeconds < 3660 ) # anywhere between 59 & 61 minutes ...     
        targetMp3 = ''.join((targetFolder, '/', str(x), '.mp3'))
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
            
    return targetFolder

           
def audioConcat (sourceFolder, audioFile = 'new', postfix = '.mp3' ):
    r'''
    Concatenates alphanumerically sorted audio files into a single audio fle.
    Uses sox command via subprocess.call
    
    Parameters
    ----------
    folder : string
        Name of folder where audio chunks already exist
    audioFile : string
        Name of target file that is the result of audio concatenation
    postfix : string
        ex: ".mp3" or ".ogg"- sox uses this to determine audio encoding for target file
        
    Returns
    -------
    audioFile : string 
        Name of newly concatenated audio file (full path name)
    '''
    current = os.getcwd()
    os.chdir(sourceFolder)
    targetFile = ''.join((audioFile, postfix))
    fullTargetPath = ''.join((sourceFolder, targetFile))
    #grab list of files in sourceFolder
    rex = ''.join(('*',postfix))
    concatList = sorted(list(glob.iglob(rex)))
    #if there are multiple audio files in the folder where we expect them ..
    if len(concatList) > 1:
        #then build sox command
        cmd = concatList
        cmd.insert(0,'sox')
        cmd.append(fullTargetPath)
        print '+++++++++++++++++++++++++++++++++++++'
        print 'audioConcat: ', cmd
        print '+++++++++++++++++++++++++++++++++++++'
        #execute sox command to concat audio files
        call(cmd)
    #else, if there is only one audio file, rename it and move it
    elif len(concatList) == 1:
        sourceFile = ''.join((sourceFolder,concatList[0]))
        os.rename(sourceFile, targetFile)
    else: # no audio files in folder
        print 'ERROR: no audio files in ',sourceFolder, ' to concat'
    #return to current working dir 
    os.chdir(current)
    print 'END: audioConcat'  
    return targetFile
          
def buildArchive (DTstart, DTend):
    r'''
    Builds audio file from the hour long archives.  Uses `DTstart` and `DTend`
    to know start and end of file.
    accepts:
        DTstart - startTime as datetime object
        DTend - startTime as datetime object
    returns:
        tempFolder: string 
            represents folder where concatted mp3 exists
        tempAudioFile: string 
            name of concatted mp3
        success: boolean 
            indicates that audio file was successfully created
    NOTE: 
        success will be set to False if an attemp is made to make
        an audio file longer than 4 hours
    '''
    # buildChunkList(DTstart, DTend)
    chunkList,success = buildChunkList(DTstart, DTend) 
    if success:
        # tempFolder is a unique folder containing audio chunks
        tempFolder = createAudioChunks(chunkList)
        # audioConcat(tempFolder)
        bigMp3 = audioConcat(tempFolder)
        return tempFolder, bigMp3, success
    else: #buildChunkList failed 
            # (a) too large archive requested <or>
            # (b) starts after it finishes
        return 'DUD', 'DUD', success
          
        
def sendArchive (sourcePath, sourceFile, remotePath, remoteFileName):
    r'''
    Parameters
    ----------
        sourcePath : string 
            represents file path of audio file
        sourceFile: string
            represents file name of audio file
        remoteFileName : string 
            represents remote target file name            
        remotePath : string 
            represents remote target folder
    Returns
    -------
        sftp : pysftp.Connection object
            # instantiating Connection object multiple layers down kinda sucks
            # gotta pass it all the way back up the stack ...
        
    '''
    
    #ftp = ftplib.FTP(key.host, key.username, key.passwd)
    sftp = pysftp.Connection(host=key.host, username=key.username, password=key.passwd)
    #ftp.cwd(remotePath)   
    print 'remote path -> ', remotePath
    print 'remote file name -> ', remoteFileName
    sftp.cwd(remotePath)

    os.chdir(sourcePath) # has been local.Mp3Staging
    #myfile = open(sourceFile, 'rb')
    print 'START: *SFTP* of audioArchive'    
    #ftp.storbinary('STOR ' + sourceFile , myfile)
    sftp.put(sourceFile, remoteFileName)
    #myfile.close()
    print 'SFTP of sendArchive COMPLETE!!!'
    
    '''
    # renaming remote file should happen somewhere else
    # Using scp, er, ftp, mv "new.mp3" to "current.mp3"
    ftp.rename(localMp3, 'current.mp3') # not really "local" mp3 anymore ...
    print 'ftp of sendArchive COMPLETE!!!'
    '''
    return sftp

def deleteFolder (folder):
    r'''
    This function deletes contents of specified (local) folder, then deletes 
    the folder itself. `folder` should not contain any subfolders.  If there
    are subfolders, this function will print an error message to stdout and 
    will return `success = False`.  Although this function is general purpose,
    It was originally intended to delete the tempFolder created by XXXX after
    the audiofile it contains has been sent to its intended destination by
    the sendArchive function
    
    Accepts
    -------
    folder: string 
        represents complete (local) folder path
    Returns
    -------
    success: boolean
        success = false if `folder` contains subdirectories (safe > sorry)
        success = true if `folder` is emptied out and deleted
    '''
    # Go to local folder
    os.chdir(folder)
    # Make list of all subdirectories
    d = '.'
    folderList = filter(lambda x: os.path.isdir(os.path.join(d, x)), os.listdir(d))
    # If list is non-empty:
    if len(folderList) > 0:
        # return success = False
        print "deleteFolder: Does not delete a folder that contains subfolders."
        print "deleteFolder: Better safe than sorry!!!"
        print "folder -> ', folder"
        success = False
        return success
    # Else: no subdirectories in folder
    else:
        # Make list of all files in folder
        xFiles = os.listdir(d)
        # Delete each file in list
        for aFile in xFiles:
            os.remove(aFile)
        # Go up in file directory
        os.chdir('..')
        # Delete folder
        os.rmdir(folder)
        # return success = True
        success = True
        return success

def renameRemoteFile (oldRemoteFile, oldRemotePath, newRemoteFile, 
                      newRemotePath = '@@SAME@@'):
    r'''
    rename a remote file.  FTP connection should already be established.
    Default = `newRemotePath` is set to match `oldRemotePath`
    '''
    if newRemotePath == '@@SAME@@':
        newRemotePath == oldRemotePath
    oldPath = ''.join((oldRemotePath, oldRemoteFile))
    newPath = ''.join((newRemotePath, newRemoteFile))
    # QUESTION: Do I need to be in the folder that contains the file in order
        # to rename the file???
    # ANSWER: Not the way I read the docs ...
    #ftp.rename(oldPath, newPath)
    sftp.rename(oldPath, newPath)
    
def uploadArchive(startTuple, endTuple, targetFolder, targetFile):
    r"""
    Creates archives with arbitrary start and end times, and uploads them to an
    arbitrary remote folder.
    Accepts:
    --------
        startTuple: datetime.tuple
            ex: startTuple = (2008, 11, 12, 13, 51, 18)
            dt_obj = DT.datetime(*startTuple[0:6])
            = 2008-Nov-12 13:51:18
        endTuple: datetime.tuple
            endTuple - startTuple should be 4 hours or less!!!
        targetFolder: string
            string that defines pathname, should end in "/"
        targetFile: string
            string that defines what archive will be named on remote target
            example: "MyCoolArchive.mp3"
            postfix of .mp3 or .ogg for example should be sufficient to set
            desired audio encoding of target file
    Returns:
    --------
        sftp : 
        success: boolean
            ftp.close() can happen after uploadArchive has been called the last 
            time
        
    """
    DTstart = DT.datetime(*startTuple[0:6]) #down to the second, no microseconds!
    DTend = DT.datetime(*endTuple[0:6])
    
    sourceFolder, sourceAudio, success = buildArchive(DTstart, DTend)
    
    if not success:
        return 'DUDsftp', success
    else:
        print 'uploadArchive line 755'
        print 'sourceFolder -> ',sourceFolder
        print 'sourceAudio -> ', sourceAudio
        print 'targetFolder -> ' , targetFolder
        print 'targetFile -> ', targetFile
        sftp = sendArchive(sourceFolder, sourceAudio, targetFolder, targetFile)
        deleteFolder(sourceFolder) # It was only a temp folder anyway
        return sftp, success
        
def new2current(startTuple, endTuple, targetFolder, targetFile = 'new.mp3',
                finalFile = 'current.mp3'):   
    r''' Creates and uploads archive to new audio file in specified remote
    folder.  Then, moves new audio file to final audio file, also in specified
    remote folder.
    '''
    sftp, success = uploadArchive(startTuple, endTuple, targetFolder, targetFile)
    targetFilePath = ''.join((targetFolder,targetFile))
    finalFilePath = ''.join((targetFolder,finalFile))
    try: # remove the target file before we move the sourceMp3 to it ...
        sftp.remove(finalFile)
    except: # or the target file is already gone 
        pass
    finally:
        print 'targetFilePath -> ',targetFilePath
        print 'finalFilePath -> ', finalFilePath
        sftp.rename(targetFilePath, finalFilePath) 
    return sftp, success    


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
#import ftplib
import pysftp

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
           
remotePath = local.remote
           
DEBUGGING = False
   

if __name__ == '__main__':
    
    tab = '    '
    #pp = pprint.PrettyPrinter(indent=4)
    
    #Now = DT.datetime.now() + relativedelta(microsecond=0)

    print '===================================================================='
    print 'UPLOAD_ARCHIVE.py ', str(DT.datetime.now() + relativedelta(microsecond=0))
    print '===================================================================='    
    
    #startDelta = local.startDelta
    #endDelta = local.endDelta
    
	'''
    rootFolder = ''.join((local.remoteStub,'Audio4/'))
    
    startTuple = (2016, 7,15,11,54,30)
    endTuple = (2016,7,15,12,2,00)
    targetFolder = rootFolder
    targetFile = 'NNN-Fri-TEST.mp3'
    sftp, success = uploadArchive(startTuple, endTuple, targetFolder, targetFile)
    print 'sftp -> ', str(sftp), ' ', str(type(sftp))
    #ftp.close()  
	'''
    ##########################################################################
    # DON'T FORGET TRAILING BACKSLASH FOR ALL PATH NAMES !!!!
    ##########################################################################
	    
    rootFolder = ''.join((local.remoteStub,'Audio3/'))
    #print 'rootFolder -> ', rootFolder
    
	'''
    ############################################################
    # THU 7/21/2016
    ############################################################
    
    # DriftlessMorning archive for 7/21/2016
    startTuple = (2016, 7,21,06,00,00)
    endTuple = (2016,7,21,8,3,00)
    targetFolder = ''.join((rootFolder, 'Thu0600/'))
    sftp, success = new2current(startTuple, endTuple, targetFolder)
    
    # LOTR archive for 7/21/2016
    startTuple = (2016, 7,21,9,00,00)
    endTuple = (2016,7,21,10,3,00)
    targetFolder = ''.join((rootFolder, 'Thu0900/'))
    sftp, success = new2current(startTuple, endTuple, targetFolder)
    
    # QueSeraSera archive for 7/21/2016
    startTuple = (2016, 7,21,10,00,00)
    endTuple = (2016,7,21,12,0,00)
    targetFolder = ''.join((rootFolder, 'Thu1000/'))
    sftp, success = new2current(startTuple, endTuple, targetFolder)

    # MLou's shoes archive for 7/21/2016
    startTuple = (2016, 7,21,13,00,00)
    endTuple = (2016,7,21,15,03,00)
    targetFolder = ''.join((rootFolder, 'Thu1300/'))
    sftp, success = new2current(startTuple, endTuple, targetFolder)
    
    # Slideman's shoes archive for 7/21/2016
    startTuple = (2016, 7,21,15,00,00)
    endTuple = (2016,7,21,17,03,00)
    targetFolder = ''.join((rootFolder, 'Thu1500/'))
    sftp, success = new2current(startTuple, endTuple, targetFolder)
    
    # Global Beat's shoes archive for 7/21/2016
    startTuple = (2016, 7,21,19,00,00)
    endTuple = (2016,7,21,17,21,00)
    targetFolder = ''.join((rootFolder, 'Thu1900/'))
    sftp, success = new2current(startTuple, endTuple, targetFolder)  
    
    # Hwy 131 Brew archive for 7/21/2016
    startTuple = (2016, 7,21,21,00,00)
    endTuple = (2016,7,21,23,03,00)
    targetFolder = ''.join((rootFolder, 'Thu2100/'))
    sftp, success = new2current(startTuple, endTuple, targetFolder)

    ############################################################
    # FRI 7/22/2016
    ############################################################
    
    # DriftlessMorning archive for 7/22/2016
    startTuple = (2016, 7, 22, 06,00,00)
    endTuple = (2016,7,22,8,3,00)
    targetFolder = ''.join((rootFolder, 'Fri0600/'))
    sftp, success = new2current(startTuple, endTuple, targetFolder)
    
    # 2ND CUP archive for 7/22/2016
    startTuple = (2016, 7, 22, 8,00,00)
    endTuple = (2016,7,22,9,3,00)
    targetFolder = ''.join((rootFolder, 'Fri0800/'))
    sftp, success = new2current(startTuple, endTuple, targetFolder)
    
    # Euphonic Schmorgasborg archive for 7/22/2016
    startTuple = (2016, 7, 22, 10,00,00)
    endTuple = (2016,7,22,12,0,00)
    targetFolder = ''.join((rootFolder, 'Fri1000/'))
    sftp, success = new2current(startTuple, endTuple, targetFolder)

    # RLE archive for 7/22/2016
    startTuple = (2016, 7, 22, 13,00,00)
    endTuple = (2016,7,22,15,03,00)
    targetFolder = ''.join((rootFolder, 'Fri1300/'))
    sftp, success = new2current(startTuple, endTuple, targetFolder)
    
    # Kitty Slick's shoes archive for 7/22/2016
    startTuple = (2016, 7, 22, 15,00,00)
    endTuple = (2016,7,22,17,03,00)
    targetFolder = ''.join((rootFolder, 'Fri1500/'))
    sftp, success = new2current(startTuple, endTuple, targetFolder)
	'''    
    # RedHot Record Jamboree archive for 7/22/2016
    startTuple = (2016, 7, 22, 19,00,00)
    endTuple = (2016,7,22,17,20,00)
    targetFolder = ''.join((rootFolder, 'Fri1900/'))
    sftp, success = new2current(startTuple, endTuple, targetFolder)  
    
    # Rick's Rock Show archive for 7/22/2016
    startTuple = (2016, 7, 22, 20,00,00)
    endTuple = (2016,7,22,22,03,00)
    targetFolder = ''.join((rootFolder, 'Fri2100/'))
    sftp, success = new2current(startTuple, endTuple, targetFolder)  
    
    #ftp.close()  
    sftp.close()
	'''
    print        
    print '++++++++++++++++++++++++++++++++++++++++++++++'
    print 'END of UploadArchiveCron -> ', str(DT.datetime.now() + relativedelta(microsecond=0))
    print '++++++++++++++++++++++++++++++++++++++++++++++'
    print



        
