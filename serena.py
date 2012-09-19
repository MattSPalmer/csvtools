#!/usr/bin/python

import desklib
import datetime as dt
import logging
import sh
import time
from collections import Counter

fn  = desklib.functions
cl  = desklib.classes
pre = desklib.presets

srn_logger = logging.getLogger('desk.serena')

def newCases():
    srn_logger.debug('\nGetting new cases.\n')
    last = fn.getEvent('last_updated_new')
    search = cl.CaseSearch(**pre.searches['new'])
    new = len([c for c in search if c.interaction_in_at > last])
    fn.updateEvents('last_updated_new', dt.datetime.now())
    if new > 0:
        n = 'case' if new == 1 else 'cases'
        fn.serenaSay(pre.phrases['new'], num=new, noun=n)

def updatedCases():
    srn_logger.debug('\nGetting updated cases.\n')
    last = fn.getEvent('last_updated')
    search = cl.CaseSearch(**pre.searches['followup'])
    updated = Counter(
            [c.user.name.split(' ')[0]
                for c in search if c.user and c.interaction_in_at > last])
    fn.updateEvents('last_updated', dt.datetime.now())
    for k, v in updated.iteritems():
        n = 'case' if v == 1 else 'cases'
        fn.serenaSay(pre.phrases['updated'],
                name=k, num=v, noun=n)

def main():
    sh.afplay('/Users/provisions/bin/csvtools/media/captain_planet.mp3')
    while True:
        newCases()
        updatedCases()
        time.sleep(30)

if __name__ == '__main__':
    main()
