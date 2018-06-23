# -*- coding: utf-8 -*-
"""
downloaded from www.bitbucket.org/spinitron on Mon Jun 29 21:13:58 2015

v0.1 - June 30
    functionality: gets JSON data from SpinPapi & converts to a python nested dict

"""

'''Python SpinPapi client

  File: SpinPapiClient.py
  Author Tom Worster
  Copyright (c) 2012 Spinitron, LLC. All rights reserved.
  Redistribution and use in source and binary forms, with or without modification, are permitted
      provided that the following conditions are met:
   * Redistributions of source code must retain the above copyright notice, this list of conditions
           and the following disclaimer.
   * Redistributions in binary form must reproduce the above copyright notice, this list of
           conditions and the following disclaimer in the documentation and/or other materials provided
           with the distribution.
   * Neither the name of the Spinitron, LLC. nor the names of its contributors may be used to endorse
           or promote products derived from this software without specific prior written permission.
  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
  IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
  FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
  IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
  OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
  '''

import hmac, hashlib, urllib, base64, sys
from time import gmtime, strftime
from operator import itemgetter

#my imports
import requests
#import simplejson as json
import json
#import ast #json parses better for me
import pickle

class SpinPapiClient:
  '''A SpinPapi client class.

    {@see http://spinitron.com/user-guide/pdf/SpinPapi-v2.pdf}
    NOTE: all SpinPapi client applications must cache result data. This
    class does not provide caching.
    '''

  def __init__(self, userid, secret, station=''):
    '''Client constructor.

      :param string userid: Authentication user ID issued by Spinitron
      :param string secret: Authentication secret issued by Spinitron
      :param string station: Station ID
      '''

    self.params = {}
    self.params['papiversion'] = '2'
    self.host = 'spinitron.com'
    self.url = '/public/spinpapi.php'
    self.params['papiuser'] = userid
    self.secret = secret
    self.params['station'] = station

  def query(self, params):
    '''Perform an uncached SpinPapi query.

      :param dict params: SpinPapi query parameters. At least method
        must be present in the dict.

      :return string: A complete signed query URL.
      '''

    # Add requested params to object default params
    all_params = self.params
    for key, val in params.iteritems():
      all_params[key] = val

    # Add current GMT timestamp to params
    all_params['timestamp'] = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())

    # Sort params alphabetically by dict key
    all_params = sorted(all_params.items(), key=itemgetter(0))

    # Build the urlencoded query in a list and join it with '&' chars
    the_query = []
    for key, val in all_params:
      the_query.append(urllib.quote(key) + '=' + urllib.quote(val))
    the_query = '&'.join(the_query)

    
    # Construct the query's HMAC signature.
    signature = self.host + '\n' + self.url + '\n' + the_query
    signature = hmac.new(self.secret, signature, hashlib.sha256)
    signature = signature.digest()
    signature = base64.b64encode(signature)
    signature = urllib.quote(signature, '')

    return ('http://' + self.host + self.url
        + '?' + the_query + '&signature=' + signature)

def dictPrint (D,indent):
    '''
    recursively print the whole damn dictionary
    '''
    
    for element in D:
        if D[element] != dict:
            print (indent * ' ') +str(element) + ':' + str(D[element])
        else:
            indent += 3
            dictPrint(D, indent)

def myGetDay(day):
    '''
    use SpinPapi to load a day
    day = integer from 0 to 7
        0 = Sunday
        1 = Monday ...
    returns a dict
    this strips off the rest of the requests get object, for better or worse
    '''
    r = requests.get(client.query({'method': 'getRegularShowsInfo', 'station': 'wdrt', 'When': str(day)}))
    d = json.loads(str(r.text))
    return d
    
def myGetSchedule(days):
    '''
    '''
    mySchedule = {}
    for i in days:
        print days[i]
        mySchedule[days[i]] = myGetDay(i)
    return mySchedule
    
def PickleDump (f,d):
    '''
    d is a nested dict containing one week of schedules
    f = string containing file location of Schedule Pickle
    '''
    F = open(f, 'wb')
    pickle.dump(d,F)
    
#MAIN
        
days = { 0: 'Sunday' , 1 : 'Monday' , 2 : 'Tuesday' , 3 : 'Wednesday' , 4 : 'Thursday' , 5 : 'Friday' , 6 : 'Saturday'}

client = SpinPapiClient('db2b837164b6385c', '868378c8f16f1c77')

SchedulePickle = 'Schedule.pkl'

'''
#this pulls data on current strong
r = requests.get(client.query({'method': 'getSong', 'station': 'wdrt'}))
print r.text
'''

#r = requests.get(client.query({'method': 'getRegularShowsInfo', 'station': 'wdrt', 'When': 'now'}))
#r = myGetDay(0)

ScheduleDict = myGetSchedule(days)

PickleDump(ScheduleDict, SchedulePickle)

#the magic that turns json into a dict
# uses 'str' to cast unicode as an old fashioned string
#d = json.loads(str(r.text))
print 
print 'd'
print type(d)

#dictPrint (d,0)

