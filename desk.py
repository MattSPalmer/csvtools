#!usr/bin/env python

import desklib.functions as fn
import desklib.classes as cl
import desklib.searches as s

def main():
    for case in cl.CaseSearch(**s.user('me')):
        print case
        for interaction in case:
            print interaction
        print '\n\n'
            

if __name__ == '__main__':
    main()
