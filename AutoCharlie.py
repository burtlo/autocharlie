# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 18:12:39 2015

@author: adude
"""

'''
cron job A
This program is intended to be called hourly as a cron job (5 min past hour)
    *searches database of radio programs, and updates audio archive for any show
        that ended in the previous hour.
    *checks to see that shows that ended in the hour before the previous hour
        actually were saved to the correct archive folder
'''

#load schedule
#create CurrentTime object
#for each show in Schedule:
    #append time sensitive attributes to show as follows:
    #aShow['TempTime'] = TempTime(aShow, aDay)

#for each day in Schedule:
    #for yesterday and today:

    #for each time slot the show plays:

        #did the show end during the previous hour?
        #if yes then:
            #grab each hour block of audio that comprises the show
            #cut and concatenate audio files as necessary
            #does ogg vorbis need to be converted to mp3 for website???
            #push newly created audio to proper folder with proper filename
                #background details

'''
cron job B
to happen soon after cron job A is done
'''

#load program database
    #??? other ways to traverse a database without loading the whole thing?

#for each show in the database:
    
    #for each time slot that the show plays:
    
        #did the show end during the time covered by the cron job A?
        #if yes, then:
            #confirm the existence of the audio file creted by cron job A
                #does it have proper name & location
                #does it have proper time of creation/update
                #does the audio file have the proper chronological length?
                #if dead air is removed from the mp3/ogg is the resulting mp3
                    #markedly shorter than the mp3 that it was derived from?