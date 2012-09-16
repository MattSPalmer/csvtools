#!usr/bin/env python

import desklib

fn = desklib.functions
cl = desklib.classes
s  = desklib.searches

def main():
    search = cl.CaseSearch(**s.searches['unassigned'])


if __name__ == '__main__':
    main()
