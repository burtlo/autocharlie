# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 22:50:17 2015

@author: adude
"""

'''
date stuff to check out:

    date.isocalendar()
       Return a 3-tuple, (ISO year, ISO week number, ISO weekday).
'''

import datetime
import time



#example of year first time format using string formatting
myDate = time.strftime("%Y-%m-%d-%X")
print myDate + str(type(myDate))

#same as above with microseconds tagged onto end of string
nowTime = datetime.datetime.now()
print
print 'nowTime ' + str(nowTime)+ '  ' + str(type(nowTime))

# 1:10pm on my facebook birthday in 2015
t = datetime.datetime(2015,6,1,13, 10, 00)
print
print 'facebook birthday 2015: ',str(t)
myDelta = nowTime - t
print
print 'myDelta: ' + str(myDelta) + '  ' + str(type(myDelta))

Delta2 = datetime.timedelta( hours = 1, minutes = -5)

print; print Delta2