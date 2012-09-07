#!usr/bin/env python

import desk
import cPickle as pickle

def weCanPickleThat(data, filename):
    out_f = open(filename, 'wb')
    try:
        pickle.dump(data, out_f, protocol=2)
    finally:
        out_f.close()

def main():
    search = desk.CaseSearch(
            assigned_user='Matt Palmer',
            status='open')

    for case in search:
        case.getInteractions()

    case = search[-1]
    weCanPickleThat(case, 'inter.dat')
    weCanPickleThat(search, 'search.dat')

if __name__ == '__main__':
    main()
