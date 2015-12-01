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

dud = datetime.datetime.now()
print dud
print 'wait 10 seconds now'
time.sleep( 5)
later = datetime.datetime.now()
print later
print later - dud
