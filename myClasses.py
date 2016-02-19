# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 15:45:49 2016

@author: lmadeo
"""
import datetime as DT
from dateutil.relativedelta import *
import calendar

class CurrentTime(object):
    '''
    CurrentTime is an object that needs to be instantiated each time 
    autoCharlie runs, presumably every hour, 15 minutes after the hour
    possible usage:
    charlieTime = CurrentTime()
    The CurrentTime object contains date/time data that all the shows in the 
        sched can reference as necessary, instead of each show maintaining its
        own copy
    '''    
    def __init__(self, aDay, now=DT.datetime.now()):
        '''
        '''
        #bump now to minute #zero of new day
        now = now + relativedelta(hour=0, minute=0, second=0, microsecond=0)
        self.now = now
        self.today = DT.date.today()
        self.num2day = { -1: 'SaturdayBEFORE', 0: 'Sunday' , 1 : 'Monday' , 
                        2 : 'Tuesday' , 
                        3 :'Wednesday',  4 : 'Thursday' , 5 : 'Friday' , 
                        6 :'Saturday', 7 : 'SundayAFTER'}
        self.week = {}
        self.week[0] = now + relativedelta(weekday = SU(-1))
        self.week[-1] = self.week[0] + relativedelta(days = -1)
        for day in range(1,8):
            self.week[day] = self.week[day-1] + relativedelta(days = +1)
            
class TempTime(object):
    '''
    CurrentTime should run first
    TempTime contains *show attributes* that need to be calculated each time
    the Sched is loaded from the drive, presumably by autoCharlie, then 
    attached to a show (see TempTime.__init__ docstring)
    '''
    Num2Day = { 0: 'Sunday' , 1 : 'Monday' , 2 : 'Tuesday' , 3 : 'Wednesday' ,
        4 : 'Thursday' , 5 : 'Friday' , 6 : 'Saturday'}
    Day2Num = {'Monday': 1, 'Tuesday': 2, 'Friday': 5, 'Wednesday': 3, 'Thursday': 4, 'Sunday': 0, 'Saturday': 6}
    def __init__(self, aShow, aDay, now = DT.datetime.now()):
        '''
        to maintain consistent definition of now, now should be passed like so:
        aShow['TempTime'] = TempTime(aShow, aDay,**charlieTime.now**)))
        '''
        self.convertedDay = 0
        self.weekday = (now.weekday()+1)
        self.HIW = 0 # HIW = Hour In Week = float in range (0 - 168)
        
    def isInHour(self, lastHour):
        '''
        get lastHour from lastCompleteHour()
        boolean
        '''
        if int(self.HIW) == lastHour:
            return True
        else:
            return False
        
    def lastCompleteHour():
        '''
        OPTION #1:
        return hour, daydelta
            hour =int (last complete hour in range [0:23])
            dayDelta = 0 if day of lastCompleteHour = today
                     = -1 if lastCompleteHour is called during the first hour 
                         of today
        
        '''
        
class SchedInfo(object):
    '''
    SchedInfo contains show attributes that I am locally tacking onto
    the Schedule that was originally grab from Spinitron via the API.
    '''
    alternationMethodList = ['Every Week','Alternate','Week of the Month']
    evenOddList = ['Even','Odd','All','N/A']
    WOTMList = [1,2,3,4,5]
    
    def __init__(self, alternationMethod ='Every Week', evenOdd = 'All', WOTMList = [1,2,3,4,5]):
        '''
        create SchedInfo object with default values
        '''
        self.alternationMethod = alternationMethod
        self.evenOdd = evenOdd
        self.weekOfTheMonth = WOTMList #how does scope deal with definitions at top of class???
        
    def __str__(self):
        tab = '    '
        print
        print tab + self.alternationMethod
        print tab + self.evenOdd
        print tab + str(self.weekOfTheMonth)
        
    def __repr__(self):

        a = str( "{* ")
        a +=  str(self.alternationMethod) + ' , '
        a +=  str(self.evenOdd) + ', '
        a +=  str(self.weekOfTheMonth) + ' *}'
        return a
        
def NegOne():
    return -1

### MAIN ###
if __name__ == '__main__':
    print 'myClasses.py'