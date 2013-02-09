# threatstreap-api.py
#
# Copyright (C) 2013 THREAT STREAM, Inc.
# This file is subject to the terms and conditions of the GNU General Public
# License version 2.  See the file COPYING in the main directory for more
# details.
import urllib2
import json


apiuser='user'
apikey='API_KEY'
query_api_url='https://api.threatstream.com'


def query_api(apiuser,apikey,resource,flags):
    url = query_api_url+resource+'/'+apiuser+apikey+flags
    print 'Query URL:'
    print ''
    print url
    print ''
    http_req = urllib2.Request(url, headers={'ACCEPT': 'application/json, text/html'})
    try:
        resp = urllib2.urlopen(http_req)
        contents = resp.read()
        return contents
    except urllib2.HTTPError, e:
        if e.code == 401:
            print 'UNAUTHORIZED, check username or API key.'
        else:
            print 'Error code: ', e.code
    except urllib2.URLError, e:
       print 'Failed to contact server'
       print 'Check proxy settings or network'
       sys.exit()
       


def api_decode(api_data):
    if api_data != None:
        # Cleanup non-ascii
        api_data = json.loads(api_data)
        results = api_data['objects']
        return results


def fetch_intel(apiuser,apikey):
   print 'Downloading intelligence: \n'
   CORE = { 'c2_domain','bot_ip'}
   for itype in CORE:
       rows = []
       c = query_api(apiuser,apikey,'intelligence','&limit=0&format=json&itype=%s' % (itype))
       data = api_decode(c)
       for i in data:
           print i