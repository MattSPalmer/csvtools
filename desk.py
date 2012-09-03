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

# }}}
# Functions {{{
def getFromDesk(category, **params):
    base_url = 'http://shopkeep.desk.com/api/v1/'
    output_format = 'json'
    request_url = '%s%s.%s?' % (base_url, category, output_format)
    for k, v in params.iteritems():
        request_url += '%s=%s&' % (k, v)
    res, content = client.request(request_url, "GET")
    if not content:
        return res
    return json.loads(content)
# }}}
# Classes {{{
    # Case {{{
class Case:
    def __init__(self, data):
        self.data = data

    def __getitem__(self, index):
        return self.data[index]

    def __repr__(self):
        pass
    # }}}
    # DeskSearchResult {{{
class DeskSearchResult:
    def __init__(self, **params):
        self.data = getFromDesk('cases', **params)
        self.count = self.data['count']
        self.results = self.data['results']
        self.total = self.data['total']
        self.page = self.data['page']
        self.cases = {}
        for result in self.results:
            caseId = result['case']['id']
            self.cases[caseId] = Case(result['case'])

    def __getitem__(self, index):
        return self.cases[index]

    def itercases(self):
        for caseId in sorted(self.cases.keys()):
            yield self.cases[caseId]
    # }}}
# }}}

def main():
    start, end = dateRange(delta=-3)
    params = {
            'count': '100',
            'status': 'new,open,pending',
            'labels': 'needs',
            'assigned_group': 'Customer'
            }
    box = DeskSearchResult(**params)
    for case in box.itercases():
        print case['subject']

if __name__ == '__main__':
    main()
