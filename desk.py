#!usr/bin/env python

import desklib.functions as fn
import desklib.classes as cl
import desklib.searches as s

def main():
    search = cl.CaseSearch(**s.searches['assigned'])
    print fn.isMoreRecent(search)

if __name__ == '__main__':
    main()
