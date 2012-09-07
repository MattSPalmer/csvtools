#!usr/bin/env python

import desklib

fn = desklib.functions
cl = desklib.classes

def main():
    start, end = fn.dateRange(delta=-3)
    params = {
            'assigned_group': 'Customer Care',
            'labels': 'Needs Update'
            }
    search = cl.CaseSearch(**params)
    print search


if __name__ == '__main__':
    main()
