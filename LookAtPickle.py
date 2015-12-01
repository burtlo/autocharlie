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
    
v.0.4 - Nov 23 - No different than recently saved v.0.3

"""

from operator import itemgetter
import SpinPapiClient as Papi
import requests
#import simplejson as json
import json
import pickle



def dictPrint (D,indent):
    '''
    recursively print the whole damn dictionary
    dud    
    '''
    
    for element in D:
        if D[element] != dict:
            print (indent * ' ') +str(element) + ':' + str(D[element])
        else:
            indent += 3
            dictPrint(D, indent)

def myGetDay(day):
    '''
    use SpinPapi to load a day
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
    days is a dict {int (0-7) : day(Sunday back to Sunday)}
    '''
    mySchedule = {}
    for i in days:
        print days[i]
        mySchedule[days[i]] = myGetDay(i)
    return mySchedule
    
def SchedScrub(ScheduleDict):
    '''
    accept SpinPapi schedule in dict format
    return schedule with unwanted crap removed, i.e.: request and success
        elements of original day schedules
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
    '''
    F = open(f, 'wb')
    pickle.dump(d,F)
    F.close()
    
def OpenPickle(SchedulePickle):
    '''
    '''
    F = open(SchedulePickle, 'rb')
    return pickle.load(F)

class shows(object):
    '''
    a dict of show objects
    '''
    def  __init__(self, Schedule):  
        self.showDict = {}
        
class show(object):
    '''
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
    
    
def OverLap(Schedule):
    '''
    return a dict of slots with overlaps
    key = Day/Start/End
    value = list( Day, Start, End,list (Shows) )
    partial overlaps will confuse this algorithm
    '''
    pass

def PrintADay(Schedule,Day):
    '''
    '''
    pass


    
    
    
#MAIN

tab = '\t'        
Days = { 0: 'Sunday' , 1 : 'Monday' , 2 : 'Tuesday' , 3 : 'Wednesday' ,
        4 : 'Thursday' , 5 : 'Friday' , 6 : 'Saturday'}
testDays = { 0: 'Sunday' , 1 : 'Monday' }

client = Papi.SpinPapiClient('db2b837164b6385c', '868378c8f16f1c77')

SpinSchedulePickle = 'SpinSchedule.pkl'
mySchedulePickle = 'mySchedule.pkl'

#the section below uses SpinPapi to grab a fresh copy of the weekly schedule
#and save two pickled versions
'''
#  do these to get fresh schedule from Spinitron
#  make accomodations to make new pickle and not overwrite old
ScheduleDict = myGetSchedule(Days)
print 'New Schedule obtained from Spinitron'
#save unadulterated data from SpinPapi
PickleDump(SpinSchedulePickle, ScheduleDict)

#strip off data I don't care about
myScheduleDict = SchedScrub(ScheduleDict)
print 'mySchedule saved as ',mySchedulePickle
#save scrubbed data
PickleDump(mySchedulePickle, myScheduleDict)
'''

Sched = OpenPickle(mySchedulePickle)
print 'Pickle Opened'

#dictPrint (d,0)

for day in Sched:
    print day
    '''
    for show in Sched[day]:
        print show
    '''

    #sort shows by start time
    Sched[day] = sorted(Sched[day], key=itemgetter('OnairTime'))
    #print selected info about shows
    for show in Sched[day]:
        '''
        print (tab + show['ShowName'])
        print (tab+tab + show['OnairTime'] + tab + show['OffairTime'])
        '''
        for thingy in show:
            print thingy + tab, show[thingy]

            
        break #cuz I just want to look at one show ...
    break
        
    # Sort params alphabetically by dict key
    #all_params = sorted(all_params.items(), key=itemgetter(0))