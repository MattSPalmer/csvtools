#!usr/bin/python

import desklib
import logging

fn  = desklib.functions
cl  = desklib.classes
pre = desklib.presets

def newCases():
    srn_logger.debug('\nGetting new cases.\n')
    last = fn.getEvent('last_updated_new')
    search = cl.CaseSearch(**pre.searches['new'])
    statuses = Counter( [c for c in search if c.interaction_in_at > last])
    fn.updateEvents('last_updated_new', dt.datetime.now())
    for k, v in statuses.iteritems():
        n = 'case' if v == 1 else 'cases'
        fn.serenaSay(pre.phrases['new'],
                name=k, num=v, noun=n)

def main():
    search = cl.CaseSearch(**pre.searches['new'])
    print len(search)

if __name__ == '__main__':
    main()
