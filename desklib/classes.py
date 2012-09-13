#!usr/bin/env python

import functions as fn
import datetime as dt
import shelve
import sys
import logging

logging.basicConfig(level=logging.ERROR)

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

class CaseSearch(DeskObject):
    def __init__(self, all_pages=False, **params):
        res, content = fn.getFromDesk('cases', **params)
        self.data = content
        self.params = params
        try:
            super(CaseSearch, self).__init__(self.data)
        except:
            logging.error('Status: %s' % res['status'])
        
        new, updated, old = fn.updateSieve(self)        
        self.cases = self.new = self.updated = self.old = {}

        for result in self.results:
            case_id = result['case']['id']
            if str(case_id) in old:
                self.cases[case_id] = self.old[case_id] = Case(case_id=case_id)
            elif str(case_id) in updated:
                self.cases[case_id] = self.updated[case_id] = Case(
                        case_id=case_id, force_update=True)
            elif str(case_id) in new:
                self.cases[case_id] = self.new[case_id] = Case(
                        data=result['case'])

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
    def __init__(self, case_id=None, data=None, force_update=False):
        if (not (case_id or data)):
            logging.error('When instantiating a Case you must specify either '
                    'the case data or case ID.')
            sys.exit()
        pref_attrs = {'case_status_type': 'status'}
        case_file = shelve.open('cases', writeback=True)

        try:
            case_id = str(int(case_id))
        except:
            pass

        if force_update:
            try:
                logging.debug('Updating case #%s...' % case_id)
                res, content = fn.getFromDesk('cases/'+case_id)
                case_file[case_id] = data = content['case']
            except NameError:
                logging.error('When specifying force_update in a case '
                        'instantiation, make sure to specify id_num too.')
                sys.exit()
            finally:
                case_file.close()
        else:
            try:
                # Try to grab case data from cache.
                data = case_file[case_id]
            except TypeError:
                # Data provided but ID not included. Store case using data from
                # case search.
                logging.debug("We have data for this case and we don't have "
                        "the case yet so let's use the data")
            except KeyError:
                # ID but no data passed. Data not in cache. Download from Desk.
                logging.debug('Downloading case #%s...' % case_id)
                res, content = fn.getFromDesk('cases/'+case_id)
                case_file[case_id] = data = content['case']
            finally:
                case_file.close()

        super(Case, self).__init__(data, pref_attrs=pref_attrs)

    def __getitem__(self, index):
        self.getInteractions()
        index = sorted(self.interactions)[index]
        return self.interactions[index]

    def __repr__(self):
       return self.output()

    def __iter__(self):
        self.getInteractions()
        for int_id, interaction in sorted(self.interactions.iteritems()):
            yield interaction

    def __len__(self):
        return len(self.interactions.keys())

    def output(self):
        lines = []
        lines.append(u"Case ID: {0.id}".format(self))
        lines.append(u"-"*len(lines[0]))
        lines.append(u"Subject: {0.subject}".format(self))
        lines.append(u"Created at: {0.created_at}".format(self))
        lines.append(u"Updated at: {0.updated_at}".format(self))
        try:
            lines.append(u"Assigned to: {0.user.name}".format(self))
        except AttributeError:
            lines.append(u"Unassigned")
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
            logging.debug('Updating interactions for case #%s...' % case_id)
            res, content = fn.getFromDesk('interactions', case_id=self.id)
            int_file[case_id] = data = content
        else:
            try:
                data = int_file[case_id]
            except KeyError:
                logging.debug('Downloading interactions for case #%s...' % case_id)
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
    def __init__(self, data):
        pref_attrs = {
                'interactionable': 'incoming'
                }
        super(Interaction, self).__init__(data, pref_attrs=pref_attrs)

    def __repr__(self):
        lines = []
        lines.append('{0.direction:>3}: {0.created_at}'.format(self))
        return '\n'.join(lines)
