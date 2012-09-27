#!/usr/bin/env python

import desklib
import datetime as dt
import logging
import os
import random
import sh
import time

fn = desklib.functions
cl = desklib.classes
pre = desklib.presets

srn_logger = logging.getLogger('desk.serena')

def playSound():
    # Gah this is so hacky.
    sound_dir = os.path.join(os.path.dirname(desklib.__file__), '../media')
    sound_files = [f for f in os.listdir(sound_dir) if 'mp3' in f]
    filename = random.choice(sound_files)
    the_file = os.path.join(sound_dir, filename)
    sh.afplay(the_file)

def newCases():
    srn_logger.debug('\nGetting new cases.\n')
    last = fn.getEvent('last_updated_new')
    search = cl.CaseSearch(**pre.searches['new'])
    new = len([c if c.interaction_in_at else True
               for c in search if c.interaction_in_at > last])
    fn.updateEvents('last_updated_new', dt.datetime.now())
    if new > 0:
        n = 'case' if new == 1 else 'cases'
        fn.serenaSay(pre.phrases['new'], num=new, noun=n)

def updatedCases():
    srn_logger.debug('\nGetting updated cases.\n')
    last = fn.getEvent('last_updated')
    search = cl.CaseSearch(**pre.searches['followup'])
    updated = {}
    for c in search:
        if c.user and c.interaction_in_at > last:
            x = c.user.name.split(' ')[0]
            y = ' '.join(list(str(c.id)))
            updated.setdefault(x, []).append(y)
    fn.updateEvents('last_updated', dt.datetime.now())
    for name, ids in updated.iteritems():
        if len(ids) > 1:
            say_ids = ', '.join(ids[:-1]) + ', and %s' % ids[-1]
        elif len(ids) == 1:
            say_ids = ids[0]

        fn.serenaSay(pre.phrases['updated'],
                     name=name, ids=say_ids)

def main():
    playSound()
    while True:
        newCases()
        updatedCases()
        time.sleep(30)

if __name__ == '__main__':
    main()