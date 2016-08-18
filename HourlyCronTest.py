# -*- coding: utf-8 -*-
"""
Created on Wed May 11 15:58:25 2016

@author: lmadeo

HourlyCronTest.py

This version of HourlyCron only exists to test the archiver_script to see that
it doesn't break anything.
The simple goal is to let this job run for a while and send mp3s to the Audio4 
folder.  Let's hope it's easy!!!!

"""

import os
import local
import key
import SpinPapiLib as SPlib

import datetime as DT
from dateutil.relativedelta import *
import calendar

import pprint

from subprocess import call

from contextlib import contextmanager
import sys

import glob
import ftplib
import pysftp

import HourlyCron as HC

# example of sox and call usage:
    # http://ymkimit.blogspot.com/2014/07/recording-sound-detecting-silence.html
# option other than subprocess.call -> os.system

#num2day has been modified to align with date.weekday() RTFM
num2day = { 7: 'SaturdayAFTER', -1: 'Sunday' , 0 : 'Monday' , 
            1 : 'Tuesday' , 2 :'Wednesday',  3 : 'Thursday' , 
            4 : 'Friday' , 5 :'Saturday', 6 : 'Sunday'}
            
num2dayShort = { 7: 'SatAFTER', -1: 'SunBEFORE' , 0 : 'Mon' , 
            1 : 'Tue' , 2 :'Wed',  3 : 'Thu' , 
            4 : 'Fri' , 5 :'Sat', 6 : 'Sun'}
            
day2shortDay = { 'Monday' : 'Mon', 'Tuesday' : 'Tue', 
                'Wednesday' : 'Wed', 'Thursday': 'Thu', 'Friday': 'Fri',
                'Saturday': 'Sat', 'Sunday': 'Sun'}
                
day2num = {'Monday':0, 'Tuesday':1, 'Wednesday':2, 'Thursday':3,
           'Friday':4, 'Saturday':5, 'Sunday':6}
           
DEBUGGING = False
   

if __name__ == '__main__':
    
    tab = '    '
    pp = pprint.PrettyPrinter(indent=4)
    
    #Now,as defined below, is actually the start of today
    Now = DT.datetime.now() + relativedelta(hour=0, minute=0, second=0, microsecond=0)

    ThisHour = DT.datetime.now() + relativedelta( minute=0, second=0, microsecond=0)
    print '===================================================================='
    print 'HOURLYCRON-*test*.py ', str(DT.datetime.now() + relativedelta(microsecond=0))
    print '===================================================================='    
    #print 'ThisHour -> ', str(ThisHour)
    
    startDelta = local.startDelta
    endDelta = local.endDelta
    startSpinDay = local.startSpinDay

    #grab most recentCharlieSched pickle out of designated folder
    charlieSched = HC.getCharlieSched()
    #pp.pprint( charlieSched )
    #add any necessary remote folders
    HC.addNewRemoteFolders(charlieSched)
    print 'dud85'    

    #LastHour is one hour ago if EndDelta is greater than zero
    LastHour, today = HC.getCurrentTime(endDelta)
    #adjust time to Spinitron time
    spinDay = HC.day2spinDay(today, LastHour, startSpinDay) #spinDay of *last archivable chunk*
    print tab, 'LastHour -> ', LastHour
    print tab, 'today -> ', today
    print tab, 'spinDay -> ', spinDay
    
    #======================================
    # make list of shows to archive
    #======================================
    if DEBUGGING:
        #changing LastHour & spinDay hijacks current time
        #showToArchive will be the Euphonic Smorgasbord (as of June 2016)
        LasthHour = 12
        spinDay = 'Friday'
    showsToArchive = HC.getShows2Archive(charlieSched, LastHour, spinDay) 
        
    print '==========================================='
    print 'showsToArchive ->'
    print tab, str(showsToArchive)
    print '=========================================='
    
    # if there's going to be something to archive, then open ftp client
    if len(showsToArchive) > 0:
        #ftp = ftplib.FTP(key.host, key.username, key.passwd)
        sftp = pysftp.Connection(host=key.host, username=key.username,
                                 password=key.passwd)
        #ftp.connect(host = key.host, port=key.port)
        #ftp.cwd(local.remote)
        sftp.chdir(local.remoteTesting)
    #================================================================
    # build mp3 for each show in list
    #================================================================
    for show in showsToArchive:
        # build list of audio archive chunks to concat
        chunkList = HC.buildChunkList(show, spinDay)
        print "====================="
        print "PrettyPrint chunkList:"
        pp.pprint(chunkList)
        print "====== END: PrettyPrint chunkList ===="
        
        # create correct mp3 for each chunk of show to archive
        HC.createAudioChunks(chunkList, local.tmpMp3)
        print 'AudioChunks created for: ', str(show)

        # sox-concat the audio fles just put into tmpMp3 folder
        HC.audioConcat(local.tmpMp3, local.Mp3Staging)
        
        #if audioConcat was successful:
        if True: # because success is the only option!
            # send "new.mp3" to correct folder on webserver, using ftp
        
            #build target folder name ex: remote file path + "Sun1300"
            timeList = show['OnairTime'].split(':')
            showStart = ''.join((timeList[0],timeList[1]))
            subfolder = ''.join((day2shortDay[spinDay], showStart)) # ex: Sun1300
            remoteTargetFolder = ''.join((local.remoteTesting, subfolder))
            #ftp.cwd(remoteTargetFolder)
            try:
                sftp.cwd(remoteTargetFolder)
            except IOError:
                sftp.mkdir(remoteTargetFolder)
                sftp.cwd(remoteTargetFolder)

            os.chdir(local.Mp3Staging)
            
            #ftp magic upload
            localMp3 = 'new.mp3'
            #myfile = open(localMp3, 'rb')
            print 'START: *SFTP* of audioArchive'    
            #ftp.storbinary('STOR ' + localMp3 , myfile)
            sftp.put(localMp3)
            #myfile.close()
            # Using scp, er, ftp, mv "new.mp3" to "current.mp3"
            #ftp.rename(localMp3, 'current.mp3') # not really "local" mp3 anymore ...
            sourceMp3 = localMp3 # to increase readability of sftp.rename ...
            try: # we will try to remove the target file before we move the sourceMp3 to it ...
                sftp.remove('current.mp3')
            except:
                pass
            finally:
                sftp.rename(sourceMp3, 'current.mp3') # not really 'local' mp3 anymore ...
                print '*SFTP* of audioArchive COMPLETE!!!'

    if len(showsToArchive) > 0:
        #ftp.close()  
        sftp.close()
    print        
    print '++++++++++++++++++++++++++++++++++++++++++++++'
    print 'END of HourlyCron-*test* -> ', str(DT.datetime.now() + relativedelta(microsecond=0))
    print '++++++++++++++++++++++++++++++++++++++++++++++'
    print



        
