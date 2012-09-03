#!usr/bin/env python

# Declarations {{{
import oauth2 as oauth
import json
import time
import datetime as dt
from confidential import desk_creds

consumer = oauth.Consumer(key=desk_creds['key'], secret=desk_creds['secret'])
token = oauth.Token(desk_creds['token'], desk_creds['token_secret'])
client = oauth.Client(consumer, token)
# }}}
# Date Tools {{{
today = dt.datetime.today()

def dtToYMD(datetimeObj):
    return datetimeObj.date().strftime('%Y%m%d')

def datetimeToEpoch(datetimeObj):
    return str(int(time.mktime(datetimeObj.timetuple())))

def timeRange(start_dt=None, end_dt=today, delta=None):
    if start_dt == None and delta == None:
        raise NameError('Remember to specify either start_dt or delta.')
    elif not start_dt:
        start_dt = end_dt + dt.timedelta(days=delta)
    return (datetimeToEpoch(start_dt), datetimeToEpoch(end_dt))

arg_hash = {
        'today': timeRange(delta=0),
        'yesterday': timeRange(delta=-1),
        'week': timeRange(delta=-7),
        'month': timeRange(delta=-30)
        }
# }}}
# Classes {{{
class CaseContainer:
    def __init__(self, category, **params):
        self.data = getFromDesk(category, **params)
        self.count = self.data['count']
        self.results = self.data['results']
        self.total = self.data['total']
        self.page = self.data['page']

    def itercases(self):
        pass
        


class Case:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        pass
# }}}
# Functions {{{
def getFromDesk(category, **params):
    base_url = 'http://shopkeep.desk.com/api/v1/'
    output_format = 'json'
    request_url = '%s%s.%s?' % (base_url, category, output_format)
    for k, v in params.iteritems():
        request_url += '%s=%s&' % (k, v)
    res, content = client.request(request_url, "GET")
    return json.loads(content)
# }}}

def main():
    params = {
            'created': 'week',
            'assigned_user': 'Patrick',
            'count': '30'
            }

    data = getFromDesk('cases', **params)

    total = data['total']
    results = data['results']

    print data.keys()
    print total
    for result in results:
        case = result['case']
        print case['subject']

if __name__ == '__main__':
    main()
