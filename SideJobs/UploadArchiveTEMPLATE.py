# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29, 2016

@author: lmadeo

UploadArchive.py

"""

import local
#from UploadArchiveLib import new2current, closeConnection
import UploadArchiveLib as UAL
import datetime as DT
from dateutil.relativedelta import relativedelta
    
remotePath = local.remote
           

print '===================================================================='
print 'UPLOAD_ARCHIVE.py ', str(DT.datetime.now() + relativedelta(microsecond=0))
print '===================================================================='    

	    
rootFolder = ''.join((local.remoteStub,'Audio3/'))

'''
###########################################################################
NOTE: ALL START AND END TIMES ARE DEMONINATED IN REAL TIME, NOT SPIN TIME
HOWEVER, TARGET FOLDERS FOLLOW SPIN TIME NAMING CONVENTION
THIS WOULD ONLY BE A POINT OF CONFUSION BETWEEN MIDNIGHT & THE START OF THE
SPIN DAY
############################################################################

####################################
EXAMPLE OF HOW TO UPLOAD AN ARCHIVE
####################################

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
If this is job is going to run on an ongoing basis, you 
will need to save this file with an informative name, then
add the file to crontab, so that it will run on a repeating
basis.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#################################################################
# EXAMPLE OF JOB THAT WILL REPEAT:
# Let's assume that cron tab will call this job once a week,
# at a time of day sonn after the desired show to archive is done 
# broadcasting.  Also, we will try to avoid overlapping this job with
# one of the cron jobs that runs 24/7, five minutes after the hour -
# we will give the cron job 10 minutes to run, so we might start this
# job @ 15 minutes after the hour ...
#################################################################
'''

# datetime object to time tuple:
# time_tuple = dt_obj.timetuple()

'''
# Nearly Noon News, on Monday
# This works if the cron job runs each Monday
now = DT.datetime.now() + relativedelta(microsecond=0)
nowtuple = now.timetuple()
startTuple =(11, 55, 0) # 11:55am
endTuple = (12, 2, 30) # 12:02:30 -just past noon
start = UAL.fullTimeTuple(startTuple, DT.datetime.now()).timetuple()
end = UAL.fullTimeTuple( endTuple, DT.datetime.now()).timetuple()
targetFolder = ''.join((rootFolder, 'NNN/Mon/'))
sftp, success = UAL.new2current(start, end, targetFolder)
'''


'''

########################################
# 2 EXAMPLES OF ONCE OFF JOBS
########################################
# Sunday @ 2pm 7/24/2016
# 2016 July 24, 14=2pm(military time), zero minutes, zero seconds
startTuple = (2016, 7,24,14,00,00)
endTuple =  (2016, 7,24,15,03,00)
# You should know what your target folder is on the remote machine
# For example: "Audio3/Sun1400" (Audio3 is specified in rootFolder, above)
targetFolder = ''.join((rootFolder, 'Sun1400/'))
sftp, success = UAL.new2current(startTuple, endTuple, targetFolder)

# Sunday @ 3pm 7/24/2016
startTuple = (2016, 7,24,15,00,00)
endTuple =  (2016, 7,24,17,03,00)
targetFolder = ''.join((rootFolder, 'Sun1500/'))
sftp, success = UAL.new2current(startTuple, endTuple, targetFolder)
'''

#########################################################
# 1st setup of Nearly Noon News audio archives
##########################################################

# Thursday NNN @ 11:55AM 7/28/2016
startTuple = (2016, 7, 28, 11,54,50)
endTuple =  (2016, 7, 28, 12,02,30)
targetFolder = ''.join((rootFolder, 'NNN/Thu/'))
sftp, success = UAL.new2current(startTuple, endTuple, targetFolder)

# Friday NNN @ 11:55AM 7/29/2016
startTuple = (2016, 7, 29, 11,54,50)
endTuple =  (2016, 7, 29, 12,02,30)
targetFolder = ''.join((rootFolder, 'NNN/Fri/'))
sftp, success = UAL.new2current(startTuple, endTuple, targetFolder)

# Monday NNN @ 11:55AM 8/1/2016
startTuple = (2016, 8,1,11,54,50)
endTuple =  (2016, 8,1,12,02,30)
targetFolder = ''.join((rootFolder, 'NNN/Mon/'))
sftp, success = UAL.new2current(startTuple, endTuple, targetFolder)

# Tuesday NNN @ 11:55AM 8/2/2016
startTuple = (2016, 8,2,11,54,50)
endTuple =  (2016, 8,2,12,02,30)
targetFolder = ''.join((rootFolder, 'NNN/Tue/'))
sftp, success = UAL.new2current(startTuple, endTuple, targetFolder)

# Wednesday NNN @ 11:55AM 8/3/2016
startTuple = (2016, 8,3,11,54,50)
endTuple =  (2016, 8,3,12,02,30)
targetFolder = ''.join((rootFolder, 'NNN/Wed/'))
sftp, success = UAL.new2current(startTuple, endTuple, targetFolder)

UAL.closeConnection(sftp)

print        
print '++++++++++++++++++++++++++++++++++++++++++++++'
print 'END of UploadArchiveCron -> ', str(DT.datetime.now() + relativedelta(microsecond=0))
print '++++++++++++++++++++++++++++++++++++++++++++++'
print



        
