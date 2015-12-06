# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 01:59:02 2015

@author: adude
CRUD
*SpinPapiTest, admin, and pickle files are currently assumed to all reside
in the same folder
"""
import SpinPapiLib as SPlib
import sys

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
    
def editShow():
    '''
    prompt admin to modify various fields of show
    '''
    
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
        show =
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
        
    goodInput = False
    print
    while not(goodInput):
        print ('Enter <1> to select show by DAY or <2> to select show by NAME'),
        reply = input('or enter <Q> to quit:  ')
        
        if reply.upper() == 'Q': # Q is for quit, you quitter
            return
            
        if reply.strip() == '1': #select day
            goodInput = True
            
            ###
            dayString = getDayString() 
            ###
            
            goodShow = False
            daySched = day2sched(dayString,Sched[dayString]) #create one-day sched 
            while not (goodShow):    
                #print day's schedule
                print; print
                SPlib.TraverseShows2(daySched,SPlib.AdminPrintShow, SPlib.myPrint)
                #select a show from a day's schedule
                reply2 = readVal( int, 'ENTER number to select show: ', 'is not an integer')
                if reply2 - 1 in range(len(daySched[dayString])):
                    goodShow = True
                    print '#TODO where to, now that show has been selected???'
                else:
                    print 'Please enter a number between 1 and '+ str(len(daySched[dayString]))

                
        elif reply.strip() == '2': #select by 1st char or substring
            goodAlpha = False
            while not goodAlpha:
                print 'enter the first letter of the show name to see all shows '
                print 'that start with that letter. OR enter any part of the show name'
                replyAlpha = input('to see all shows that contain substring.')
                if len(replyAlpha) == 1:
                    goodAlpha = True
                    #seach for first char(showname) = replyAlpha by ShowName, Day of Week
                    #make list of dicts
                        #each dict --> ShowName, ShowDay
                    #For each dict in list:
                        #Print enumerated number + ShowName + ShowDay
                if len(replyAlpha) > 1:
                    goodAlpha = True
                    #grep for replyAlpha in ShowName field of every show/day
                    #make list of dicts
                        #each dict --> ShowName, ShowDay
                    #For each dict in list:
                        #Print enumerated number + ShowName + ShowDay
                else: #must be an empty string
                    pass
        else:
            print 'Get with the program!!!'
            
#MAIN
            
if sys.version[0] == '2': input = raw_input #alias py2 to py3

if __name__ == '__main__':

    #print SPlib.Days
    print; print
        
    SchedulePickle = 'Sched2.pkl'
    
    WDRTsched = loadSchedule(SchedulePickle)
    
    selectShow(WDRTsched)

