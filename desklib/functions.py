#!usr/bin/env python

###############
#  Functions  #
###############

import datetime as dt
import urllib as ul
import api
import time
import json
import logging
import shelve

logging.basicConfig(level=logging.DEBUG)

today = dt.datetime.today()

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
    case_file = shelve.open('cases')
    case_items = {}
    for result in search.results:
        case_id = str(result['case']['id'])
        case_items[case_id] = formatDeskDate(result['case']['updated_at'])
    case_ids = case_items.keys()
    updated_ids = []
    new_cases = []
    try:
        for key in case_ids:
            try:
                if (case_items[key] >
                        formatDeskDate(case_file[key]['updated_at'])):
                    updated_ids.append(key)
                    case_ids.remove(key)
                else:
                    pass
            except KeyError:
                new_cases.append(key)
                case_ids.remove(key)
    finally:
        case_file.close()

    return (case_ids, updated_ids, new_cases)
