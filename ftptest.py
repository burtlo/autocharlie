# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 19:51:02 2016

@author: lmadeo
"""

import SpinPapiLib as SPLib
import time
import local
import key
from copy import deepcopy

import pprint
from ftplib import FTP


def dudFunc(day):
    '''
    used by shced2charlieSched as a default action of doing nothing
    '''
    pass


def createRemoteFolder(timeslot):
    '''
    local.remote
    '''
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(timeslot)  
    tempList = timeslot.split('-') #split timeslot @ dashes ex: 'Sat-20:00:00-22:00:00'
    timeList = tempList[1].split(':') #split start time ex: 15:00:00
    destFolder = ''.join((tempList[0],timeList[0], timeList[1]))
    print targetStr
    
def startFTP():
    '''
    '''
    print key.host
    print key.username
    print key.passwd
    ftp = FTP(key.host, key.username, key.passwd)
    
# MAIN
    
startFTP()
    
print  "!Rd0Fr0mTh3Gr0undUp!" == key.passwd