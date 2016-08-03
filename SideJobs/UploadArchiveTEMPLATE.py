# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29, 2016

@author: lmadeo

UploadArchive.py

"""

import local
from UploadArchiveLib import new2current, closeConnection
import datetime as DT
from dateutil.relativedelta import relativedelta
    
remotePath = local.remote
           

print '===================================================================='
print 'UPLOAD_ARCHIVE.py ', str(DT.datetime.now() + relativedelta(microsecond=0))
print '===================================================================='    

	    
rootFolder = ''.join((local.remoteStub,'Audio3/'))

'''
####################################
EXAMPLE OF HOW TO UPLOAD AN ARCHIVE
####################################

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
If this is job is going to run on an ongoing basis, you 
will need to save this file with an informative name, then
add the file to crontab, so that it will run on a repeating
basis.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

===============================================================
I have failed to consider the steps necessary to set time
*relative* to the time the job runs.  This is necessary to have
a job that runs repetitively ...
===============================================================
# Sunday @ 2pm 7/24/2016
# 2016 July 24, 14=2pm(military time), zero minutes, zero seconds
startTuple = (2016, 7,24,14,00,00)
endTuple =  (2016, 7,24,15,03,00)
# You should know what your target folder is on the remote machine
# For example: "Audio3/Sun1400" (Audio3 is specified in rootFolder, above)
targetFolder = ''.join((rootFolder, 'Sun1400/'))
sftp, success = new2current(startTuple, endTuple, targetFolder)

# Sunday @ 3pm 7/24/2016
startTuple = (2016, 7,24,15,00,00)
endTuple =  (2016, 7,24,17,03,00)
targetFolder = ''.join((rootFolder, 'Sun1500/'))
sftp, success = new2current(startTuple, endTuple, targetFolder)
'''

closeConnection(sftp)

print        
print '++++++++++++++++++++++++++++++++++++++++++++++'
print 'END of UploadArchiveCron -> ', str(DT.datetime.now() + relativedelta(microsecond=0))
print '++++++++++++++++++++++++++++++++++++++++++++++'
print



        
