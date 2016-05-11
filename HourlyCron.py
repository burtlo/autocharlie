# -*- coding: utf-8 -*-
"""
Created on Wed May 11 15:58:25 2016

@author: lmadeo

hourlyCron.py

# FIRST, MOST BASIC ITERATION
-----------------------------

* Grab startDelta and endDelta from local.py

* Open most recent charlieSched in folder specified in local.py

* Build list of shows that ended in last hour
    #note this should be a two hour delay to enable tacking on of endDelta

* For each show in list:
    * build mp3 using pysox
    * send "new.mp3" to correct folder on webserver, using scp
    * Using scp, mv "new.mp3" to "current.mp3"
    
    
# FINE TUMING / FURTHER ITERATION
---------------------------------

* Error checking:
    *target folder exists? If not, create, and log an error
    *local autocharlie folder exists?  If not, create folder, then kick off
        WeeklyCron job
    

"""

