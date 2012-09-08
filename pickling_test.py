#!usr/bin/env python

import desklib
import shelve

fn = desklib.functions
cl = desklib.classes


def getShelvedCase(case_id):
    case_id = str(case_id)
    case_file = shelve.open('cases', writeback=True)
    try:
        return case_file[case_id]
    except KeyError:
        print 'downloading...'
        case_file[case_id] = cl.Case(case_id)
        return case_file[case_id]
    finally:
        case_file.close()

def main():
    for i in range(8040, 8240):
        print getShelvedCase(i).subject


if __name__ == '__main__':
    main()
