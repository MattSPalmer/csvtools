#!usr/bin/env python

import functions as fn
import datetime as dt
import sys
import logging

#############
#  Classes  #
#############

class DeskObject(object):
    def __init__(self, data, pref_attrs={}):
        self.data = data
        for k, v in self.data.iteritems():
            k = pref_attrs.get(k, k)
            try:
                v = fn.formatDeskDate(v)
            except:
                pass
            try:
                setattr(self, k, DeskObject(v))
            except:
                setattr(self, k, v)

    def __repr__(self):
        return str(self.data)

class Interaction(DeskObject):
    def __init__(self, data):
        pref_attrs = {
                'interactionable': 'incoming'
                }
        super(Interaction, self).__init__(data, pref_attrs=pref_attrs)

class Case(DeskObject):
    def __init__(self, id_num=None, data=None):
        # TODO add logic for all argument eventualities
        pref_attrs = {'case_status_type': 'status'}
        if not data:
            res, content = fn.getFromDesk('cases/'+id_num)
            try: 
                data = content['case']
            except:
                logging.error('Status: %s' % res['status'])
                logging.error(content)
        super(Case, self).__init__(data, pref_attrs=pref_attrs)

    def __getitem__(self, index):
        self.ensureInteractions()
        index = sorted(self.interactions)[index]
        return self.interactions[index]

    def __repr__(self):
       return self.output()

    def __iter__(self):
        self.ensureInteractions()
        for int_id, interaction in sorted(self.interactions.iteritems()):
            yield interaction

    def output(self):
        lines = []
        print self.data['subject']
        lines.append(u"Case ID: {0.id}".format(self))
        lines.append(u"-"*len(lines[0]))
        lines.append(u"Subject: {0.subject}".format(self))
        lines.append(u"Assigned to: {0.user}".format(self))
        lines.append(u"Status: {0.status}".format(self))
        if self.status in ['resolved', 'closed']:
            lines.append(u"Resolved at {0.resolved_at}".format(self))
        lines.append("")
        return '\n'.join(lines).encode('utf-8')

    def getInteractions(self):
        self.interactions = {}
        res, content = fn.getFromDesk('interactions', case_id=self.id)
        try:
            for result in content['results']:
                theInteraction = result['interaction']
                interaction_id = theInteraction['id']
                self.interactions[interaction_id] = Interaction(theInteraction)
            return self.interactions
        except:
            logging.error('Status: %s' % res['status'])

    def ensureInteractions(self):
        try:
            self.interactions
        except:
            self.getInteractions()

    def getLastInteraction(self):
        last_interaction = self.interactions['results'][-1]['interaction']
        email_text = last_interaction['interactionable']['email']['body']
        return (last_interaction['created_at'], email_text)

class CaseSearch(DeskObject):
    def __init__(self, all_pages=False, **params):
        res, content = fn.getFromDesk('cases', **params)
        self.data = content
        self.params = params
        self.pref_attrs = {
                'currentPage': 'page',
                }
        try:
            super(CaseSearch, self).__init__(self.data, pref_attrs=self.pref_attrs)
        except:
            logging.error('Status: %s' % res['status'])
        self.pages = divmod(self.total, self.count)[0] + 1
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
                newpage = fn.getFromDesk('cases',
                        page=pagenum, **params)['results']
                self.results += newpage
        for result in self.results:
            caseId = result['case']['id']
            self.cases[caseId] = Case(data=result['case'])
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
        index = sorted(self.cases)[index]
        return self.cases[index]

    def __iter__(self):
        for caseId in sorted(self.cases.keys()):
            yield self.cases[caseId]

    def listCases(self):
        return sorted(self.cases.keys())
    
    def refresh(self):
        __init__(self)
