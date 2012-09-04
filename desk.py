#!usr/bin/env python

# Declarations {{{
import datetime as dt
import oauth2 as oauth
import json
import sys
import time
import urllib as ul
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
    request_url = '%s%s.%s?%s' % (base_url, category, output_format,
            ul.urlencode(params))
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
        if self.data['user']:
            self.user = self.data['user']['name']
        else:
            self.user = 'unassigned'
        self.subject = self.data['subject']
        self.status = self.data['case_status_type']
        self.id_num = int(self.data['id'])
        self.resolved_at = self.data.get('resolved_at', None)

    def __getitem__(self, index):
        return self.data[index]

    def __repr__(self):
       return self.output()

    def output(self):
        lines = []
        print self.data['subject']
        lines.append(u"Case ID: {0.id_num}".format(self))
        lines.append(u"-"*len(lines[0]))
        lines.append(u"Subject: {0.subject}".format(self))
        lines.append(u"Assigned to: {0.user}".format(self))
        lines.append(u"Status: {0.status}".format(self))
        if self.data['case_status_type'] in ['resolved', 'closed']:
            lines.append(u"Resolved at {0.resolved_at}".format(self))
        return '\n'.join(lines).encode('utf-8')
    # }}}
    # CaseSearch {{{
class CaseSearch:
        # __init__ {{{
    def __init__(self, all_pages=False, **params):
        self.data = getFromDesk('cases', **params)
        self.params = params
        self.count = self.data['count']
        self.results = self.data['results']
        self.total = self.data['total']
        self.pages = divmod(self.total, self.count)[0] + 1
        self.currentPage = self.data['page']
        self.cases = {}
        if all_pages:
            if self.total > 300:
                choice = raw_input(
                        'There are {0} cases to download. '
                        'Are you sure? (y/n) '.format(self.total))
                if choice not in ('y', 'ye', 'yes', 'yea', 'yeah'):
                    print "That's probably the responsible choice. Exiting..."
                    sys.exit()
            for pagenum in range(1, self.pages):
                progress = int(100 * pagenum / float(self.pages))
                sys.stdout.write("Download progress: %d%%   \r" % (progress) )
                sys.stdout.flush()
                newpage = getFromDesk('cases',
                        page=pagenum, **params)['results']
                self.results += newpage
        for result in self.results:
            caseId = result['case']['id']
            self.cases[caseId] = Case(result['case'])
        # }}}
    def __repr__(self):
        lines = []

        now = dt.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        
        lines.append("Search run at {}".format(now))
        lines.append("="*len(lines[0])+'\n')
        lines.append('{:<55}'.format('Parameters'))
        lines.append('{:<55}'.format('-'*55))
        for k, v in sorted(self.params.iteritems()):
            lines.append("{0:<27}:{1:>27}".format(k, v))
        lines.append('\n{0} cases over {2} pages, {1} cases per page.'
                .format(self.total, self.count, self.pages))
        return '\n'.join(lines)

    def __getitem__(self, index):
        return self.cases[index]

    def itercases(self):
        for caseId in sorted(self.cases.keys()):
            yield self.cases[caseId]

    def refresh(self):
        __init__(self)
    # }}}
# }}}

def main():
    start, end = dateRange(delta=-3)
    params = {
            'assigned_group': 'Customer Care',
            'labels': 'Needs Update'
            }
    search = CaseSearch(**params)
    print search

if __name__ == '__main__':
    main()
