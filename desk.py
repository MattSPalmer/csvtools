#!usr/bin/env python

import desklib
import datetime as dt
from collections import Counter

fn   = desklib.functions
cl   = desklib.classes
pre  = desklib.presets


def main():
    search = cl.CaseSearch(**pre.searches['followup'])
    statuses = Counter([c.user.name.split(' ')[0] for c in search if c.user])
    for k, v in statuses.iteritems():
        n = 'case' if v == 1 else 'cases'
        fn.serenaSay(pre.serephra['updated'], name=k, noun=n, num=v)

if __name__ == '__main__':
    main()
