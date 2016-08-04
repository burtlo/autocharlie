# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29, 2016

NNN-cron.py

"""

import local
#from UploadArchiveLib import new2current, closeConnection
import UploadArchiveLib as UAL
import datetime as DT
from dateutil.relativedelta import relativedelta
    
remotePath = local.remote
           

print '===================================================================='
print 'NNN-cron.py ', str(DT.datetime.now() + relativedelta(microsecond=0))
print '===================================================================='    

	    
rootFolder = ''.join((local.remoteStub,'Audio3/'))

# datetime object to time tuple:
# time_tuple = dt_obj.timetuple()

# Nearly Noon News, this job should run Mon - Fri @ 12:15
now = DT.datetime.now() + relativedelta(microsecond=0)
aday = UAL.num2dayShort(now.weekday()) # 3 letter string (ex: 'Mon')
nowtuple = now.timetuple()
startTuple =(11, 55, 0) # 11:55am
endTuple = (12, 2, 30) # 12:02:30 -just past noon
start = UAL.fullTimeTuple(startTuple, DT.datetime.now()).timetuple()
end = UAL.fullTimeTuple( endTuple, DT.datetime.now()).timetuple()
targetFolder = ''.join((rootFolder, 'NNN/',aday,'/'))
sftp, success = UAL.new2current(start, end, targetFolder)


UAL.closeConnection(sftp)

print        
print '++++++++++++++++++++++++++++++++++++++++++++++'
print 'END of NNN-cron -> ', str(DT.datetime.now() + relativedelta(microsecond=0))
print '++++++++++++++++++++++++++++++++++++++++++++++'
print



        
