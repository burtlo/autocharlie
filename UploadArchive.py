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

# Sunday @ 2pm 7/24/2016
startTuple = (2016, 7,24,14,00,00)
endTuple =  (2016, 7,24,15,03,00)
targetFolder = ''.join((rootFolder, 'Sun1400/'))
sftp, success = new2current(startTuple, endTuple, targetFolder)

# Sunday @ 3pm 7/24/2016
startTuple = (2016, 7,24,15,00,00)
endTuple =  (2016, 7,24,17,03,00)
targetFolder = ''.join((rootFolder, 'Sun1500/'))
sftp, success = new2current(startTuple, endTuple, targetFolder)

'''
############################################################
# THU 7/21/2016
############################################################

# DriftlessMorning archive for 7/21/2016
startTuple = (2016, 7,21,06,00,00)
endTuple = (2016,7,21,8,3,00)
targetFolder = ''.join((rootFolder, 'Thu0600/'))
sftp, success = new2current(startTuple, endTuple, targetFolder)

# LOTR archive for 7/21/2016
startTuple = (2016, 7,21,9,00,00)
endTuple = (2016,7,21,10,3,00)
targetFolder = ''.join((rootFolder, 'Thu0900/'))
sftp, success = new2current(startTuple, endTuple, targetFolder)

# QueSeraSera archive for 7/21/2016
startTuple = (2016, 7,21,10,00,00)
endTuple = (2016,7,21,12,0,00)
targetFolder = ''.join((rootFolder, 'Thu1000/'))
sftp, success = new2current(startTuple, endTuple, targetFolder)

# MLou's shoes archive for 7/21/2016
startTuple = (2016, 7,21,13,00,00)
endTuple = (2016,7,21,15,03,00)
targetFolder = ''.join((rootFolder, 'Thu1300/'))
sftp, success = new2current(startTuple, endTuple, targetFolder)

# Slideman's shoes archive for 7/21/2016
startTuple = (2016, 7,21,15,00,00)
endTuple = (2016,7,21,17,03,00)
targetFolder = ''.join((rootFolder, 'Thu1500/'))
sftp, success = new2current(startTuple, endTuple, targetFolder)

# Global Beat's shoes archive for 7/21/2016
startTuple = (2016, 7,21,19,00,00)
endTuple = (2016,7,21,17,21,00)
targetFolder = ''.join((rootFolder, 'Thu1900/'))
sftp, success = new2current(startTuple, endTuple, targetFolder)  

# Hwy 131 Brew archive for 7/21/2016
startTuple = (2016, 7,21,21,00,00)
endTuple = (2016,7,21,23,03,00)
targetFolder = ''.join((rootFolder, 'Thu2100/'))
sftp, success = new2current(startTuple, endTuple, targetFolder)

############################################################
# FRI 7/22/2016
############################################################

# DriftlessMorning archive for 7/22/2016
startTuple = (2016, 7, 22, 06,00,00)
endTuple = (2016,7,22,8,3,00)
targetFolder = ''.join((rootFolder, 'Fri0600/'))
sftp, success = new2current(startTuple, endTuple, targetFolder)

# 2ND CUP archive for 7/22/2016
startTuple = (2016, 7, 22, 8,00,00)
endTuple = (2016,7,22,9,3,00)
targetFolder = ''.join((rootFolder, 'Fri0800/'))
sftp, success = new2current(startTuple, endTuple, targetFolder)

# Euphonic Schmorgasborg archive for 7/22/2016
startTuple = (2016, 7, 22, 10,00,00)
endTuple = (2016,7,22,12,0,00)
targetFolder = ''.join((rootFolder, 'Fri1000/'))
sftp, success = new2current(startTuple, endTuple, targetFolder)

# RLE archive for 7/22/2016
startTuple = (2016, 7, 22, 13,00,00)
endTuple = (2016,7,22,15,03,00)
targetFolder = ''.join((rootFolder, 'Fri1300/'))
sftp, success = new2current(startTuple, endTuple, targetFolder)

# Kitty Slick's shoes archive for 7/22/2016
startTuple = (2016, 7, 22, 15,00,00)
endTuple = (2016,7,22,17,03,00)
targetFolder = ''.join((rootFolder, 'Fri1500/'))
sftp, success = new2current(startTuple, endTuple, targetFolder)
   
# RedHot Record Jamboree archive for 7/22/2016
startTuple = (2016, 7, 22, 19,00,00)
endTuple = (2016,7,22,17,20,00)
targetFolder = ''.join((rootFolder, 'Fri1900/'))
sftp, success = new2current(startTuple, endTuple, targetFolder)  

# Rick's Rock Show archive for 7/22/2016
startTuple = (2016, 7, 22, 20,00,00)
endTuple = (2016,7,22,22,03,00)
targetFolder = ''.join((rootFolder, 'Fri2100/'))
sftp, success = new2current(startTuple, endTuple, targetFolder)  
'''

closeConnection(sftp)

print        
print '++++++++++++++++++++++++++++++++++++++++++++++'
print 'END of UploadArchiveCron -> ', str(DT.datetime.now() + relativedelta(microsecond=0))
print '++++++++++++++++++++++++++++++++++++++++++++++'
print



        
