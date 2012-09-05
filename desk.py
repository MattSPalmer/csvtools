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

def formatDeskDate(date):
    date_format = '%Y-%m-%dT%H:%M:%S'
    split_date = date.split('-')
    adj_date = '-'.join(split_date[:-1])
    return dt.datetime.strptime(adj_date, date_format)

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
            self.cases[caseId] = Case(data=result['case'])
        # }}}
    def __repr__(self):
        lines = []

        now = dt.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        
        lines.append("Search run at {}".format(now))
        lines.append("="*len(lines[0])+'\n')
        lines.append('{:<45}'.format('Parameters'))
        lines.append('{:<45}'.format('-'*45))
        for k, v in sorted(self.params.iteritems()):
            lines.append("{0:<22}:{1:>22}".format(k, v))
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
    # Case {{{
class Case(object):
    def __init__(self, id_num=None, data=None):
        # TODO add logic for all argument eventualities
        preferred_attrs = {'case_status_type': 'status'}
        if not data:
            data = getFromDesk('cases/'+id_num)['case']
        self.data = data
        for k, v in self.data.iteritems():
            k = preferred_attrs.get(k, k)
            try:
                v = formatDeskDate(v)
            except:
                pass
            setattr(self, k, v)


    def __getitem__(self, index):
        return self.data[index]

    def __repr__(self):
       return self.output()

    def output(self):
        lines = []
        print self.data['subject']
        lines.append(u"Case ID: {0.id}".format(self))
        lines.append(u"-"*len(lines[0]))
        lines.append(u"Subject: {0.subject}".format(self))
        lines.append(u"Assigned to: {0.user}".format(self))
        lines.append(u"Status: {0.status}".format(self))
        if self.data['case_status_type'] in ['resolved', 'closed']:
            lines.append(u"Resolved at {0.resolved_at}".format(self))
        lines.append("")
        return '\n'.join(lines).encode('utf-8')

    def getInteractions(self):
        self.data['interactions'] = getFromDesk('interactions',
                case_id=self.id_num)
        self.interactions = self.data['interactions']
        return self.interactions

    def getLastInteraction(self):
        try:
            self.data['interactions']
        except KeyError:
            self.getInteractions()
        last_interaction = self.interactions['results'][-1]['interaction']
        email_text = last_interaction['interactionable']['email']['body']
        return (last_interaction['created_at'], email_text)


    # }}}
    # Interaction {{{
class Interaction():
    def __init__(self):
        pass

    def __getitem__(self, index):
        pass

    def __repr__(self):
        pass

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
