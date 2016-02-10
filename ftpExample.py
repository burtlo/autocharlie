# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 15:50:57 2016

ftp upload example from stackOverflow
http://stackoverflow.com/questions/12613797/python-script-uploading-files-via-ftp
"""

import ftplib
import key

username = key.username
passwd = key.passwd

fname = 'mySchedule.pkl'
targetURL = 'www.wdrtradio.org'

session = ftplib.FTP(targetURL, username, passwd)
file = open(fname,'rb')                  # file to send
session.storbinary('STOR '+fname, file)     # send the file
file.close()                                    # close file and FTP
session.quit()