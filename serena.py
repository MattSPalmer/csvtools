#!/usr/bin/env python

import desklib
import datetime as dt
import logging
import os
import sh
import time
from collections import Counter

fn = desklib.functions
cl = desklib.classes
pre = desklib.presets

srn_logger = logging.getLogger('desk.serena')

def sound(name):
    # Gah this is so hacky.
    dir = os.path.join(os.path.dirname(desklib.__file__), '..')
    sh.afplay(os.path.join(dir,'media/{}.mp3'.format(name)))

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
        [c.user.name.split(' ')[0] for c in search
         if c.user and c.interaction_in_at > last])
    fn.updateEvents('last_updated', dt.datetime.now())
    for k, v in updated.iteritems():
        n = 'case' if v == 1 else 'cases'
        fn.serenaSay(pre.phrases['updated'],
                     name=k, num=v, noun=n)

def main():
    sound('youre_welcome')
    while True:
        newCases()
        updatedCases()
        time.sleep(30)

if __name__ == '__main__':
    main()
