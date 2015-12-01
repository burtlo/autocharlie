# -*- coding: utf-8 -*-
"""
proudly developed in the studios of WDRT, Viroqua, Wisconsin

v0.1 - June 30
    functionality: gets JSON data from SpinPapi & converts to a python nested dict
    
v0.2 - July 9
    python dict is pickled in two versions : (a) unmolested, and (b) stuff I don't 
    want is stripped out (results dict is kept, success & request dicts are 
    stripped out)
    
v.0.3 - July 9
    SpinPapiTest is now separated from SpinPapiClient
    
v.0.4 - Nov 23 - Added notes on desired dict elements to add

"""
'''
current Dict structure: ( run LookAtPickle.py for more insight)
Day
    Show
        Scheduled (boolean)
        ShowDescription
        ShowID  
            ??Can I find other instances of the same show on diff days, based on ShowID?
        Weekdays 
            ??Does Monday view block a full list of days that a show plays??
        OnAirTime
        OffAirTime
        ShowUrl
        ShowCategory
        ShwowUsers [{UserID:,DJName:}]
        ShowName
        
elements to add to Show dict:
        StartRecDelta
            negative is earlier, positive is later
            hour: minute format, with plus or minus prefix
            default to zero, since shows seem to be either on time or late
        EndRecDelta
            negative is earlier, positive is later
            hour: minute format, with plus or minus prefix
            default to +5 to catch end of overrunning shows
                or default to start plus 4 hours for DRMC regulations
        Folder
            file folder location to put mp3 archive file
        Subshow - boolean
            True if show is a segment within another show
            This will prevent SchedLinter from posting an error
            for double-booked shows
'''
from operator import itemgetter
import SpinPapiClient as Papi
import requests
#import simplejson as json
import json
import pickle
import copy

def uniFix(uniStr):
    '''
    hack to replace common unicode characters that do not have an 
    ascii equivalent
    code lifted from here:
        http://www.intelligent-artifice.com/2010/02/how-to-filter-out-common-unwanted-characters-in-python.html
    presentation:
        http://farmdev.com/talks/unicode/
    '''
    text = uniStr
    character_replacements = [
    ( u'\u2018', u"'"),   # LEFT SINGLE QUOTATION MARK
    ( u'\u2019', u"'"),   # RIGHT SINGLE QUOTATION MARK
    ( u'\u201c', u'"'),   # LEFT DOUBLE QUOTATION MARK
    ( u'\u201d', u'"'),   # RIGHT DOUBLE QUOTATION MARK
    ( u'\u201e', u'"'),   # DOUBLE LOW-9 QUOTATION MARK
    ( u'\u2013', u'-'),   # EN DASH
    ( u'\u2026', u'...'), # HORIZONTAL ELLIPSIS
    ( u'\u0152', u'OE'),  # LATIN CAPITAL LIGATURE OE
    ( u'\u0153', u'oe')   # LATIN SMALL LIGATURE OE
    ]
    for (undesired_character, safe_character) in character_replacements:
         text = text.replace(undesired_character, safe_character)
    return text


            
def dictPrint (D,indent):
    '''
    recursively print the whole damn dictionary
    TODO:
        key and value of dict need to be handled differently
 
    '''

    if type(D) == dict:
        for el in D:
            print (indent * ' ') + '{';
            dictPrint(D[el],indent+3)
            print '}'
    if type(D) == list:
        for el in D:
            print(indent * ' ') + '[';
            dictPrint(el, indent+3)
            print ']'
    if type(D) == str:
        print D;
    elif type(D) == unicode:
        print uniFix(D);
    else: #maybe int, float, or bool???
        print str(D)
       
            
            

def myGetDay(day):
    '''
    use SpinPapi to load a day from Spinitron
    day = integer from 0 to 7
        0 = Sunday
        1 = Monday ...
    returns a dict
    this strips off the rest of the requests.get object, for better or worse
    '''
    r = requests.get(Papi.client.query({'method': 'getRegularShowsInfo', 'station': 'wdrt', 'When': str(day)}))
    d = json.loads(str(r.text))
    return d
    
def myGetSchedule(days):
    '''
    get sched from Spinitron
    days is a dict {int (0-7) day(Sunday back to Sunday) : list/dict of shows
    	during that day} 
    
    #TODO research to see if there are two copies of Sunday
	
    '''
    mySchedule = {}
    for i in days:
        print days[i]
        mySchedule[days[i]] = myGetDay(i)
    return mySchedule
    
def SchedScrub(ScheduleDict):
    '''
    accept output from myGetSchedule (SpinPapi schedule converted to
        dict format)
    return schedule with unwanted crap removed, i.e.: remove  "request" 
        and "success" elements of original day schedules and keep
        "results"
    '''
    mySched = {}
    for day in ScheduleDict:
        mySched[day] = ScheduleDict[day]['results']
    return mySched
    
def PickleDump (f,d):
    '''
    d is a nested dict containing one week of schedules
    actually, d can be about any damn thing
    f = string containing file location of Schedule Pickle
    goes to default/current directory
    '''
    F = open(f, 'wb')
    pickle.dump(d,F)
    F.close()
    
def OpenPickle(SchedulePickle):
    '''
    returns serialized schedule, or any other pickled object
    note:
        serialized and saved to disk is synonymouse with pickled
    '''
    F = open(SchedulePickle, 'rb')
    return pickle.load(F)

class shows(object):
    '''
    a dict of show objects
    not using this right now 11/27/2015
    '''
    def  __init__(self, Schedule):  
        self.showDict = {}
        
class show(object):
    '''
    not using this right now ... 11/27/2015
    '''
    def __init__(self, papiShow):
        pass
    
    def BuildShowDict(Schedule):
        '''
        take a week's (scrubbed) schedule
        and return a dict of show objects
        '''
        pass

def BuildDJdict(Schedule):
    '''
    take a week's (scrubbed) schedule
    and return a dict of DJs
    '''
    pass
    
    
def OverLap(Schedule):
    '''
    return a dict of slots with overlaps
    key = Day/Start/End
    value = list( Day, Start, End,list (Shows) )
    partial overlaps will confuse this algorithm
    '''
    pass

def PrintAShow(Show):
    '''
    A show is a dict?
    '''
    print type(show)
    

def dudFunc():
    '''
    used by TraverseShows as a default action of doing nothing
    '''
    pass

def myPrint(anObject):
    '''
    kind of a hack
    '''
    print anObject

def PrettyPrintShow(show):
    '''
    can be used in conjunction with TraverseShows to print formatted schedule
    '''
    tab = '   '    
    print (tab + show['ShowName'])
    print (tab+tab + show['OnairTime'] + tab + show['OffairTime'])    

def TraverseShows (Schedule, showFunc = dudFunc, dayFunc = dudFunc):
    '''
    showFunc will execute once everytime we get to a show during
        the traversal
    dayFunc will execute once everytime we get to a day during the traversal
    showFunc is a function that accepts a show as a parameter
    NOTE: If a show occurs on 5 different days, TraverseShows will go
        to each day instance of that show separately
    '''
    for day in Schedule:
        dayFunc (day)
        #sort shows by start time
        Schedule[day] = sorted (Schedule[day], key=itemgetter('OnairTime'))
        for show in Schedule[day]:
            showFunc(show)    
    
def SchedtoSched2(Sched):
    '''
    This function accepts a schedule (in the format that SchedScrub() creates
    and adds the following elements to each show
    
    '''
#MAIN

tab = '\t'        
Days = { 0: 'Sunday' , 1 : 'Monday' , 2 : 'Tuesday' , 3 : 'Wednesday' ,
        4 : 'Thursday' , 5 : 'Friday' , 6 : 'Saturday'}
testDays = { 0: 'Sunday' , 1 : 'Monday' }

client = Papi.SpinPapiClient('db2b837164b6385c', '868378c8f16f1c77')


mySchedule2Pickle = 'mySchedule2.pkl'


def FreshPapi():
    '''
    #TODO  make accomodations to make new pickle and not overwrite old
    
    This function
    uses SpinPapi to grab a fresh copy of the weekly schedule
    and save two pickled versions
    SpinSchedule is the schedule obtained from Spinitron via SpinPapi
    SchedulePickle1 is the cleaned up version of SpinSchedule
    Schedule1 replaces mySchedule
    In another function, SchedulePickle2 will take SpinSchedule1 
        and add further desired fields
    '''
    
    Days = { 0: 'Sunday' , 1 : 'Monday' , 2 : 'Tuesday' , 3 : 'Wednesday' ,
            4 : 'Thursday' , 5 : 'Friday' , 6 : 'Saturday'}
            
    #SpinSchedulePickle contains an unadulterated copy of the schedule
    #as obtained from Spinitron via SpinPapi
    SpinSchedulePickle = 'SpinSchedule.pkl'
        
    Schedule1Pickle = 'Schedule1.pkl'
    #mySchedulePickle = 'mySchedule.pkl' 
        #this is old version of Schedule1Pickle
        #myShedulePickle should still be on file ...

    #TODO  make accomodations to make new pickle and not overwrite old
    SpinScheduleDict = myGetSchedule(Days)
    print 'New Schedule obtained from Spinitron'
    
    #save unadulterated data from SpinPapi to Pickle
    #current directory as it now stands
    PickleDump(SpinSchedulePickle, SpinScheduleDict)
    
    #strip off data I don't care about
    ScheduleDict1 = SchedScrub(SpinScheduleDict)
    print 'Schedule1 saved as ',Schedule1Pickle
    #save scrubbed data to a second Pickle file
    PickleDump(Schedule1Pickle, ScheduleDict1)


mySchedulePickle = 'mySchedule.pkl'
Sched = OpenPickle(mySchedulePickle)
print 'Pickle Opened'

#dictPrint (d,0)

TraverseShows(Sched,PrettyPrintShow, myPrint)

'''
for day in Sched:
    print day
    
    #for show in Sched[day]:
        #print show
    

    #sort shows by start time
    Sched[day] = sorted(Sched[day], key=itemgetter('OnairTime'))
    #print selected info about shows
    for show in Sched[day]:
        print (tab + show['ShowName'])
        print (tab+tab + show['OnairTime'] + tab + show['OffairTime'])
        
        
    # Sort params alphabetically by dict key
    #all_params = sorted(all_params.items(), key=itemgetter(0))

for i in 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx':
    print
dictPrint2 (Sched['Monday'], 3)
'''