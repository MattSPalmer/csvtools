#!usr/bin/env python

import desklib.functions as fn
import desklib.classes as cl
import desklib.searches as s

def main():
    for case in cl.CaseSearch(**s.user('Stephen')):
        print case
        if case[-1].direction == 'in':
            print 'Needs Update'
        else:
            print 'Everything is Fine'
        print


if __name__ == '__main__':
    main()
