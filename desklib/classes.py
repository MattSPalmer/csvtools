#!usr/bin/env python

import functions as fn
import datetime as dt
import shelve
import sys
import logging

#############
#  Classes  #
#############

class DeskObject(object):
    """
    The base object class for data structures obtained through Desk's API.

    Rather than have each class extend 'object', they extend DeskObject and
    thereby inherit its useful practice of drilling down recursively through a
    dictionary-based structure and transforming the respective keys and values
    into a system of nested attributes, which is much cleaner to deal with when
    coding.

    For instance, we receive from Desk in JSON:

        {
        'case': {
            'id':'1',
            'created_at': '2012-09-01',
            'user': {
                'id': '1',
                'name': 'Matt'
                }
            # etc...
            }
        }

    Upon instantiation, the DeskObject class take this data (in dictionary
    format) and returns nicely nested attributes thusly:

        case.id == 1
        case.created_at == '2012-09-01'
        case.user.id == 1
        case.user.name == 'Matt'

    Extended by:

    CaseSearch
    Case
    Interaction
    """

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

class CaseSearch(DeskObject):
    """
    A data container of Case instances informed by an API call to Desk.com based
    on parameters passed as an argument. 

    Methods:

    __init__: TODO

    __repr__: TODO

    __getitem__: TODO

    __len__: TODO

    __iter__: TODO

    listCases: TODO

    refresh: TODO

    """
    def __init__(self, all_pages=False, force_update=False, **params):
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
            self.cases[caseId] = Case(caseId, force_update=force_update)

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

    def __len__(self):
        return len(self.cases)

    def __iter__(self):
        for caseId in sorted(self.cases.keys()):
            yield self.cases[caseId]

    def listCases(self):
        return sorted(self.cases.keys())
    
    def refresh(self):
        __init__(self)

class Case(DeskObject):
    """
    TODO: Case documentation
    """
    def __init__(self, id_num, force_update=False):
        pref_attrs = {'case_status_type': 'status'}
        case_id = str(id_num)
        case_file = shelve.open('cases', writeback=True)
        if force_update:
            print 'Updating case #%s...' % case_id
            res, content = fn.getFromDesk('cases/'+case_id)
            case_file[case_id] = data = content['case']
            case_file.close()
        else:
            try:
                data = case_file[case_id]
            except KeyError:
                print 'Downloading case #%s...' % case_id
                res, content = fn.getFromDesk('cases/'+case_id)
                case_file[case_id] = data = content['case']
            finally:
                case_file.close()

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

    def __len__(self):
        return len(self.interactions.keys())

    def output(self):
        lines = []
        print self.subject
        lines.append(u"Case ID: {0.id}".format(self))
        lines.append(u"-"*len(lines[0]))
        lines.append(u"Subject: {0.subject}".format(self))
        lines.append(u"Created at: {0.created_at}".format(self))
        lines.append(u"Assigned to: {0.user.name}".format(self))
        lines.append(u"Status: {0.status}".format(self))
        if self.status in ['resolved', 'closed']:
            lines.append(u"Resolved at {0.resolved_at}".format(self))
        lines.append("")
        return '\n'.join(lines).encode('utf-8')

    def getInteractions(self, force_update=False):
        self.interactions = {}
        case_id = str(self.id)
        int_file = shelve.open('interactions', writeback=True)

        if force_update:
            print 'Updating interactions for case #%s...' % case_id
            res, content = fn.getFromDesk('interactions', case_id=self.id)
            int_file[case_id] = data = content
        else:
            try:
                data = int_file[case_id]
            except KeyError:
                print 'Downloading interactions for case #%s...' % case_id
                res, content = fn.getFromDesk('interactions', case_id=self.id)
                int_file[case_id] = data = content
            finally:
                int_file.close()
        try:
            for result in data['results']:
                theInteraction = result['interaction']
                interaction_id = theInteraction['id']
                self.interactions[interaction_id] = Interaction(theInteraction)
            return self.interactions
        except:
            logging.error('Status: %s' % res['status'])
            sys.exit()

class Interaction(DeskObject):
    """
    TODO: Interaction documentation
    """
    def __init__(self, data):
        pref_attrs = {
                'interactionable': 'incoming'
                }
        super(Interaction, self).__init__(data, pref_attrs=pref_attrs)

    def __repr__(self):
        lines = []
        lines.append('{0.direction:>3}: {0.created_at}'.format(self))
        return '\n'.join(lines)
