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
import ftplib


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
    FYI: instantiating ftplib twice doesn't cause an error
    '''
    ftp = ftplib.FTP(key.host, key.username, key.passwd)
    #ftp = ftplib.FTP(key.host, key.username, key.passwd)
    return ftp
    
# MAIN
    
ftp = startFTP()
current = ftp.pwd()
print current
print ftp.nlst()

'''
try:
    ftp.cwd('/wdrtradio.org/Audio3')
except ftplib.error_perm:
    print 'no pre-existing Audio3 folder'
    ftp.mkd('/wdrtradio.org/Audio3')
    print 'Audio3 has been created'
'''
    
#ftp.mkd('Audio3')