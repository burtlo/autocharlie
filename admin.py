# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 01:59:02 2015

@author: adude
CRUD
*SpinPapiTest, admin, and pickle files are currently assumed to all reside
in the same folder

0.1
    what was committed on Dec 6 @ 1:30pm
    
0.2 - meh, don't do this, a list of dicts should work
    convert from Sched[day] is a list of dicts
        to Sched[day] is a dict of dicts
        key will be an integer, shows will be sorted in each day
        key will be unique within day, buy keys will be reused in
            different days
        this will break a bunch of functions!!!
        
12/7/2015
    Test tail end of selectShow code
    selectShow is good
    now editShow needs help recursion is a diversion
    




"""
import SpinPapiLib as SPlib
import sys
import re

def to6columns(DJList):
    '''
    accepts DJList
    returrns a list of rows, each row has 6 elements (3 pairs of ID#/DJName)
    last row is padded with empty strings, if necessary
    QQQ edge cases of very short DJList???


    '''
    def myAppend(destRow,SrcDict):
        destRow.append('<'+str(SrcDict['UserID'])+'>')
        destRow.append(SrcDict['DJName'])
        return destRow
    rows = []
    numrows = len(DJList)//3 # number of rows in target list of rows, 6 columns per row
    for x in range(numrows):
        y = x + numrows
        z = x + 2*numrows
        #make rows[x] a list with 6 elements for pretty printing
        rows.append([])
        rows[x] = myAppend(rows[x],DJList[x])
        rows[x] = myAppend(rows[x],DJList[y])
        rows[x] = myAppend(rows[x],DJList[z])
    if len(DJList) % 3 == 1:
        rows.append([])
        rows[numrows] = myAppend(rows[numrows],DJList[len(DJList)-1])
        rows[numrows].extend(['',''])
        rows[numrows].extend(['',''])
    elif len(DJList) % 3 == 2:
        rows.append([])
        rows[numrows] = myAppend(rows[numrows],DJList[len(DJList)-2])
        rows[numrows] = myAppend(rows[numrows],DJList[len(DJList)-1]) 
        rows[numrows].extend(['',''])
    return rows
        
def prettyPrintDJs(DJList):
    '''
    accepts DJList
    prints out list of userIDs + DJNames in 6 columns
    '''
    rows = to6columns(DJList)
    widths = [max(map(len, map(str,col))) for col in zip(*rows)]
    for row in rows:
        print " ".join((val.ljust(width) for val, width in zip(row, widths)))
        
        
def loadSchedule(filename, directory=''):
    '''
    serialized/pickled Schedule
    '''  
    if directory == '': #TODO concat directory + filename
        return SPlib.OpenPickle(filename)
    else:
        print 'error: non-current working directory search not implemented'

def saveSchedule(filename, SchedDict, directory):
    '''
    serialized/pickled Schedule
    perhaps tage date onto filename to have a log of previous schedules???
    '''
    if directory == '': #TODO concat directory + filename
        SPlib.PickleDump(filename, SchedDict)
    else:
        print 'error: non-current working directory search not implemented'
        
def addShow():
    '''
    prompt admin for all the info
    '''
    
def deleteShow():
    '''
    show will be deleted in all time slots that it exists
    '''
def editUser(aUser):
    '''
    '''
    pass

def createUser(DJName):
    '''
    assign UserID = max(allUserIDs) + 1
    TODO: This function not tested yet, as of 12/17/2015 !!!!!
    '''
    newUser = {}
    newUser['DJName'] = DJName
    DJList = SPlib.BuildDJList(WDRTsched)
    newUser['UserID'] = max([ x['UserID'] for x in DJList]) + 1
    return newUser

def editUserList(userList):
    '''
    edits user list for a particular show in a particular time slot
    returns updated list of users
    '''
    UL = userList
    #display UserList(of show)
    for U in UL:
        print tab+'<'+ str(U['UserID']) + '>' + tab + U['DJName']
    reply = ''
    msgOne = 'Options: ENTER <A> to add user, <D> to delete a user, or press <ENTER> to edit next field'
    errorMsg = "Don't even know how you got here!!!"
    msg2 = 'ENTER <Number> of existing DJ to add to ShowUsers for this Show '
    msg3 = 'or <C> to Create a totally-new-to-WDRT DJ '
    msg4 = 'or hit <ENTER> to move on to next field'
    
    while reply != 'Quit':
        #options: <A> add user, <D> delete user

        reply = readCharVal('Quit','ad', msgOne, errorMsg)
    
        #display list of available DJs
        print
        print '=============AVAILABLE DJs:==================='
        prettyPrintDJs(DJList)
        #acceptable list = UserIDs + 'c'
        DJIDList = [x['UserID'] for x in DJList]
        acceptableList = map(str,DJIDList) #cast ints to strings
        acceptableList.append('c') #c for create new DJ
        #case: add user
        if reply == 'A': #add DJ to this show's ShowUsers
            #options: select DJ to ad, create new DJ to add, or <return> to exit
            reply2 = readVal3(acceptableList,msg2+msg3+msg4,'number please, or <c>, or <enter>')
            if reply2 == 'Quit':
                reply = 'Quit' # let's get all the way out of here
                break
            elif reply2 == 'C':  #create new DJ
                ExistingDJs = [x['DJName'] for x in DJList]
                #no naming conventions currently imposed on newDJName
                newDJName = readVal4(ExistingDJs, 'Enter name of new DJ','This DJ already exists')
                newUser = createUser(newDJName)
                #add newUser to userList
                UL.append(newUser)
                #update overall DJList
                DJList.append(newUser) #UserID sorting will remain intact
            #add pre-existing DJ to this show's UserList
            else: #what can reply2 be besides a legit UserID, type = str???
                for x in DJList:
                    if x['UserID'] == int(reply2):
                        UL.append(x)
                        break
                #add pre-existing DJ to this show's userList
                print '====UPDATED ShowUser List for'+ aShow['ShowName'] + '==========='
                prettyPrintDJs(UL)

        #case: delete user
        if reply == 'D':
            UserIDList = [x['UserID'] for x in UL]
            prettyPrintDJs(UL)
            #pick DJ to delete from this show, or return to Exit
            reply3 = readVal3( dud, dud, dud)

    
    
def editShow(aShow):
    '''
    prompt admin to modify various fields of show
    '''
    a = aShow
    print 'For each show attribute, enter new value, or press <ENTER> to'
    print 'leave the show attribute unchanged.'
    a['ShowName'] = readVal2(a['ShowName'],str,'ShowName-> '+a['ShowName'],"whatchoo doin' Willis?")
    #we won't edit a['Weekdays'] right now
    a['Scheduled'] = readVal2(a['Scheduled'],bool,'Scheduled-> '+str(a['Scheduled']), 'Only True and False are valid!')
    a['ShowDescription'] = readVal2(a['ShowDescription'],str,'ShowDescription-> '+'"'+ a['ShowDescription']+'"', 'How did you enter a non-string???')
    a['ShowID'] = readVal2(a['ShowID'],int,'ShowID-> '+str(a['ShowID'])+ ' do not modify this value','enter a *number*')
    #TODO time validation using time & date objects    
    a['OnairTime'] = readVal2(a['OnairTime'],str, "OnairTime -> " + a['OnairTime'],'how you enter non-string???')
    a['OffairTime'] = readVal2(a['OffairTime'],str, "OffairTime -> " + a['OffairTime'],'how you enter non-string???') 
    #TODO validate url 
    a['ShowUrl'] = readVal2(a['ShowUrl'],str, 'ShowURL -> '+'"' + a['ShowUrl']+'"', 'just looking for a string ...')
    a['ShowCategory'] = readVal2(a['ShowCategory'],str,'ShowCategory-> ' + a['ShowCategory'], "I'm all strung out")
    print
    print 'ShowUsers -> '
    a['ShowUsers'] = editUserList(a['ShowUsers'])
    #edit all new fields that I have added
         
def displayDay():
    pass

def displayShow():
    pass
    
def schedLint():
    '''
    look for overlapping shows
    and possible other problems with schedule
    '''
    
def day2sched(dayString, day):
    '''
    recieves a day, which is a list of shows and a dayString and 
    returns a one-day Schedule, with dayString as the key and day as the value
    each show is a dict of show attributes
    '''
    tempSched = {}
    tempSched[dayString] = day
    return tempSched
    
def readCharVal(default, acceptable,requestMsg, errorMsg):
    '''
    accept input string and determine if val[0] is in list of
    acceptable inputs
    acceptable is a simple string, instead of a list of single chars
    default is the return value if user enters empty string
    '''
    acceptable = acceptable.upper()
    while True:
        val = input(requestMsg + ' ')
        if val == '':
            return default
        if val[0].upper() in acceptable:
            return val[0].upper()
            
def readVal4(excluded, requestMsg, errorMsg, valType = int, default = 'Quit'):
    '''
    accept input string and validate that it is *not* on the *list* of excluded inputs
        ints in acceptable list have already been cast to strings
        if the string does not represent an int, only the first char counts
        for validation
    if val = '' return default value
    '''
#TODO fix this to resemble recent changes to readVal3    
    while True:
        val = input(requestMsg + ' ')
        if val == '':
            return default
        if val not in excluded:
            if type(val) == str:
                return val[0].upper()
            if type(val) == int:
                return val
        print errorMsg

            
def readVal3(acceptableList, requestMsg, errorMsg, valType = int, default = 'Quit'):
    '''
    accept input string and validate that it is in the *list* of acceptable inputs
        ints in acceptable list have already been cast to strings
        if the string does not represent an int, only the first char counts
        for validation
    if val = '' return default value
    '''
    
    while True:
        val = input(requestMsg + ' ')
        if val == '':
            return default

        try: #cheesy way to test for valType
            val = valType(val) #is it the desired type?
            val = str(val)
            if val in acceptableList:
                return int(val)
            else:
                print val + ' ' + errorMsg
        except ValueError:
            if val[0].upper() in acceptableList:
                return val[0].upper()
            print val + ' ' + errorMsg 

     
        

def readVal2(default, valType, requestMsg, errorMsg):
    '''
    accept input string and validate that it successfully translates
    to the desired data type
    if val = '' return default value (generally unaltered original value)
    '''
    
    while True:
        val = input(requestMsg + ' ')
        if val == '':
            return default
        try:
            #afraid to try
            #val = type(oldVal)(val) to cast new val to type of oldVal
            val = valType(val)
            return val
        except ValueError:
            print val + ' ' + errorMsg  
            
def readVal(valType, requestMsg, errorMsg):
    '''
    accept input string and validate that it successfully translates
    to the desired data type
    '''
    while True:
        val = input(requestMsg + ' ')
        try:
            val = valType(val)
            return val
        except ValueError:
            print val + ' ' + errorMsg
            
def ShowRegEx (Schedule, myRegEx):
    '''
    returns a list of shows where the ShowName attribute matches the
    received regular expression (myRegEx)
    List of shows is specified as a list of tuples:
        (ShowName,Day,OnairTime, OffairTime)
    '''
    tempList = []
    for day in Schedule:

        #sort shows by start time
        Schedule[day] = sorted (Schedule[day], key=SPlib.itemgetter('OnairTime'))
        for (x,show) in enumerate(Schedule[day]):
            ShowName = Schedule[day][x]['ShowName']
            
            if re.search(myRegEx,Schedule[day][x]['ShowName'].upper()):
                OnairTime = Schedule[day][x]['OnairTime']
                OffairTime = Schedule[day][x]['OffairTime']
                tempList.append((ShowName, day, OnairTime, OffairTime))
                
    return tempList
                
            
def selectShow(Sched):
    '''
    The following characteristics should be sufficient to uniquely define a 
    show:
        ShowName
        Day
        StartTime
            ex: There are two shows called Undercurrents on Sunday, one that
            starts midnight, the other starts at 1a.m
    returns:
        show =Sched[day][list-index]
    '''

    def getDayString():
        '''
        solicit input from user, get a number from 1 -7 that corresponds with 
        a day of the week.  Returns an alpha string for that day
        ex: 'Monday'  see SpinPapiLib.days
        '''
        
        goodDay = False
        goodInput = ['1','2','3','4','5','6','7']
        while not(goodDay):
            print;
            for key in SPlib.Days:
                print '<'+str(key+1)+'>   '+ SPlib.Days[key]
            selectedDay = input ('Enter number to select a day:  ')
            #print 'selectedDay = '+ selectedDay
                
            if selectedDay not in goodInput: #bad input
                print 'Select a number that correpsonds with a day!!'
                print 'Get with the program, dood'
            else:
                dayString = SPlib.Days[int(selectedDay)-1]
                goodDay = True 
        return dayString
        
    Sched = SPlib.makeChronological(Sched)
    goodInput = False
    print
    while not(goodInput):
        print ('Enter <1> to select show by DAY or <2> to select show by NAME'),
        reply = input('or enter <Q> to Quit:  ')
        
        if reply.upper() == 'Q': # Q is for quit, you quitter
            return #exit selectShow, nothing returned, means quitting time
            
        if reply.strip() == '1': #select day
            goodInput = True
            
            ###
            dayString = getDayString() 
            ###
            
            goodShow = False
            daySched = day2sched(dayString,Sched[dayString]) #create one-day sched 
            while not (goodShow):    
                print; print
                #print day's schedule
                SPlib.TraverseShows2(daySched,SPlib.AdminPrintShow, SPlib.myPrint)
                #select a show from a day's schedule
                reply2 = readVal( int, 'ENTER number to select show: ', 'is not an integer')
                listIndex = reply2 -1 
                if listIndex in range(len(daySched[dayString])):
                    goodShow = True
                    return Sched[dayString][listIndex] #exit selectShow() here
                else:
                    print 'Please enter a number between 1 and '+ str(len(daySched[dayString]))

                
        elif reply.strip() == '2': #select by 1st char or substring
            goodInput = True
            goodSearchString = False
            while not goodSearchString:
                print
                print 'Enter the first letter of the show name to see all shows '
                print 'that start with that letter. OR enter any part of the show name',
                replyAlpha = input('to see all shows that contain substring. -->  ')
                if len(replyAlpha) == 1:
                    goodSearchString = True
                    myRegEx = '^' + replyAlpha.upper()
                    ShowList = ShowRegEx(Sched, myRegEx)
                    #TODO showlist = showlist + RegEx, somehow stripping 'the' from the beginning of the line

                if len(replyAlpha) >= 1:
                    goodSearchString = True
                    myRegEx = replyAlpha.upper()
                    ShowList = ShowRegEx(Sched, myRegEx)
                else: #must be an empty string
                    print "Why you hit return?!?!"
                    continue
                    
                #at this point, we have created a showList
                #see function: ShowRegEx()
                if len(ShowList) == 0:
                    print; print 'No matches.  So Sorry!!!'; print
                    goodSearchString = False
                else:
                    goodSearchString = True
            goodShow = False
            while not goodShow:
                #print show list
                for x, S in enumerate(ShowList):
                    print '<'+str(x+1)+'>' +S[0]
                    print tab + S[1] + tab + S[2] + tab + S[3] 
                #solicit choice
                goodChoice = False
                while not goodChoice:
                    showPick = readVal(int,'select a show from list above: ','Please enter an integer')
                    if not(showPick - 1 in range(len(ShowList))):
                        continue
                    else:
                        goodChoice = True # this line not necessary ...
                        return Sched[ShowList[showPick-1][1]][showPick - 1] #exit selectShow() here

                
        else:
            print 'Get with the program!!!'
            continue #goto while not goodInput and try again
            
#MAIN
tab = '\t'            
if sys.version[0] == '2': input = raw_input #alias py2 to py3

if __name__ == '__main__':

    #print SPlib.Days
    print; print
        
    SchedulePickle = 'Sched2.pkl'
    
    WDRTsched = loadSchedule(SchedulePickle)
    
    DJList = SPlib.BuildDJList(WDRTsched)
    #prettyPrintDJs(DJList)

        

    aShow = selectShow(WDRTsched)
    print; print #aShow
    newShow = editShow(aShow)
    print; print newShow
