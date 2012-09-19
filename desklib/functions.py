#!usr/bin/python

###############
#  Functions  #
###############

import datetime as dt
import urllib as ul
import api
import time
import json
import sh
import shelve

today = dt.datetime.today()

# Date functions

def dtStrToDtObj(date_str):
    return dt.datetime.strptime(date_str, '%Y%m%d')

def dtObjToYMD(datetimeObj):
    return datetimeObj.date().strftime('%Y%m%d')

def dtObjToEpoch(datetimeObj):
    return str(int(time.mktime(datetimeObj.timetuple())))

def dateRange(start_dt=None, end_dt=today, delta=None):
    if start_dt == None and delta == None:
        raise NameError('Remember to specify either start_dt or delta.')
    elif not start_dt:
        start_dt = end_dt + dt.timedelta(days=delta)
    return (dtObjToEpoch(start_dt), dtObjToEpoch(end_dt))

def daysSince(days):
    datetimeObj = dt.datetime.now() - dt.timedelta(days=days)
    return dtObjToEpoch(datetimeObj)

def formatDeskDate(date):
    date_format = '%Y-%m-%dT%H:%M:%S'
    split_date = date.split('-')
    adj_date = '-'.join(split_date[:-1])
    return dt.datetime.strptime(adj_date, date_format)


def getFromDesk(category, **params):
    base_url = 'http://shopkeep.desk.com/api/v1/'
    output_format = 'json'
    request_url = '%s%s.%s?%s' % (base_url, category, output_format,
            ul.urlencode(params))
    res, content = api.client.request(request_url, "GET")
    content = json.loads(content)
    while content.get('error', False):
        logging.warning("Waiting 30 seconds to respect Desk's API") 
        time.sleep(30)
        res, content = api.client.request(request_url, "GET")
        content = json.loads(content)
    return (res, content)

def updateSieve(search):
    cache_file = shelve.open('cases')
    cache = set([ (x[0], x[1]['updated_at']) for x in cache_file.items() ])
    desk = set([ (str(x.values()[0]['id']), x.values()[0]['updated_at'])
                for x in search.results ])

    new =     set([n[0] for n in desk]) - set(n[0] for n in cache)
    novel =   desk - cache
    updated = set([n[0] for n in novel]) - new
    old =     set(n[0] for n in cache) - updated

    return map(list, (new, updated, old))

def updateEvents(k, v):
    events_file = shelve.open('events', writeback=True)
    try:
        events_file[k] = v
    except:
        print "Hey."
    finally:
        events_file.close()
    return v

def getEvent(k):
    events_file = shelve.open('events', writeback=True)
    try:
        v = events_file.get(k, None)
    except:
        print "Hey."
    finally:
        events_file.close()
    return v

def serenaSay(msg, **params):
    sh.say(msg.format(**params))
