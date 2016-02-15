# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 15:45:49 2016

@author: lmadeo
"""

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