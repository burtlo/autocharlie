# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 23:03:03 2016

@author: lmadeo
"""

# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
myText = "blah-blah.txt"
fp = open(myText, 'rb')
# Create a text/plain message
msg = MIMEText(fp.read())
fp.close()

# me == the sender's email address
me = "djgravy@mwt.net"
# you == the recipient's email address
you = "lmadeo@wdrt.org"
msg['Subject'] = 'The contents of %s' % myText
msg['From'] = me
msg['To'] = you

# Send the message via our own SMTP server, but don't include the
# envelope header.
#s = smtplib.SMTP('localhost')
s = smtplib.SMTP(host='smtp.mwt.net', port=587)
s.sendmail(me, you, msg.as_string())
s.quit()

#server = smtplib.SMTP(host='smtp.gmail.com', port=587)