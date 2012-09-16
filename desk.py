#!usr/bin/env python

import desklib.functions as fn
import desklib.classes   as cl
import desklib.searches  as s

def main():
    res, content = fn.getFromDesk('cases', s.searches['assigned'])
    for k, v in content.iteritems():
        pass


if __name__ == '__main__':
    main()
