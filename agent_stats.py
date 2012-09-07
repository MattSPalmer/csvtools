#!usr/bin/env python

import desk
import cPickle as pickle

def weCanPickleThat(data, filename):
    out_f = open(filename, 'wb')
    try:
        pickle.dump(data, out_f)
    finally:
        out_f.close()

def main():
    case = desk.CaseSearch(
            assigned_user='Matt Palmer',
            status='open')[-1]

    weCanPickleThat(case, 'nointer.dat')
    case.getInteractions()
    weCanPickleThat(case, 'inter.dat')

if __name__ == '__main__':
    main()
