#!/usr/bin/env python

import desklib
import datetime as dt
import logging
import os
import random
import sh
import time
from collections import Counter

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
    updated = Counter(
        [c.user.name.split(' ')[0] for c in search
         if c.user and c.interaction_in_at > last])
    fn.updateEvents('last_updated', dt.datetime.now())
    for k, v in updated.iteritems():
        name = pre.name_subs.get(k, k)
        n = 'case' if v == 1 else 'cases'
        fn.serenaSay(pre.phrases['updated'],
                     name=name, num=v, noun=n)

def main():
    import argparse
    import textwrap

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            Serena monitors Desk.com for activity and reports audibly when
            relevant.
            '''))

    parser.add_argument(
        '-r', '--reset', action='store_true',
        help="artificially shift the 'last_updated' timestamp back a day")

    parser.add_argument(
        '--delay', default=30,
        help="artificially shift the 'last_updated' timestamp back a day")

    args = parser.parse_args()

    if args.reset:
        fn.updateEvents(
            'last_updated',
            dt.datetime.now() - dt.timedelta(days=1))

    playSound()    
    while True:
        newCases()
        updatedCases()
        time.sleep(args.delay)

if __name__ == '__main__':
    main()
