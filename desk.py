#!usr/bin/env python

import desklib

fn = desklib.functions
cl = desklib.classes
s  = desklib.searches

def main():
    params = {
            'status': 'new,open,pending',
            'assigned_user': 'Patrick'
            }
    search = cl.CaseSearch(**params)
    print search
    for case in search:
        print case


if __name__ == '__main__':
    main()
