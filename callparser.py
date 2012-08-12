#!/usr/bin/env python

import csvtools
import typeutil
from collections import Counter
from confidential import agentKeys

# Decorators
def benchmark(func):
    """A decorator that prints the time a function takes
    to execute."""
    import time
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print func.__name__, time.clock()-t
        return res
    return wrapper

def logging(func):
    """
    A decorator that logs the activity of the script.
    (it actually just prints it, but it could be logging!)
    """
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print func.__name__, args, kwargs
        return res
    return wrapper

# Output functions
def missed(calls):
    """Given a report detailing incoming calls, print data on calls missed
    organized by date."""
    # Instantiate a Report instance from a file (most likely passed as an argument)
    # Using Report's toDict method, obtain the list of agent phone numbers by
    # call received.
    breakdown   = calls.toDict()['transfer_to_number']
    # From that list, filter only the calls that were not answered.
    missed      = dict(Counter(breakdown))['']
    period      = typeutil.days(calls.toDict()['date_added'])

    print "%s\n%s\n%d out of %d, %d days. Average: %d a day.\n" % (
            args.reportfile, len(args.reportfile)*'=', missed, len(breakdown),
            len(period), missed / len(period))

    for k, v in period.iteritems():
        print '%s/%s: %d' % (k[0], k[1], v)

def agents(calls):
    """Given a report detailing incoming calls, return and print a dict of
    the form: {name/number of agent}: {number of calls answered}"""
    breakdown   = calls.toDict()['transfer_to_number']
    agentdict   = dict(Counter(breakdown))
    for agentNum, callNum in agentdict.iteritems():
        agentNumPretty = typeutil.formatPhoneNum(agentNum)
        agentName = agentKeys.get(agentNumPretty, agentNumPretty)
        print agentName, ':', callNum
    print ''

def callers(calls):
    """Given a report detailing incoming calls, return the incoming phone
    numbers and the number of times called."""
    calls.filter('transfer_to_number', '', inverse=True)
    incoming = dict(Counter(calls.toDict()['ani']))
    for k, v in incoming.iteritems():
        print k, v

def byhour(calls):
    """Given a report detailing incoming calls over a specific date range,
    return a bar graph of hourly calls per day."""
    import operator
    import os

    # clear the terminal window
    os.system('clear')

    # prepare for readable dates
    monthhash = {
        1:  'January',
        2:  'February',
        3:  'March',
        4:  'April',
        5:  'May',
        6:  'June',
        7:  'July',
        8:  'August',
        9:  'September',
        10: 'October',
        11: 'November',
        12: 'December'}

    # isolate date strings and convert to date format from string
    dates = calls.toDict()['date_added']

    # hash the hours of each call to the day of each call.
    days = {}
    for i in dates:
        day = (i.year, i.month, i.day)
        days[day] = days.get(day, [])
        days[day].append(i.hour)

    # reduce the value of each key from a list to a count per hour
    for j in days.keys():
        days[j] = dict(Counter(days[j]))

    # creating and drawing the graph for each day (key) and set of hour counts (values)
    for day, hours in sorted(days.iteritems()):
        graph = []
        hourstring = ''

        # What day are we looking at?
        graph.insert(0, '{0} {1}, {2}\n'.format(monthhash[day[1]], day[2], day[0]))

        # A horizontal axis of hours of the day
        for n in range(0, 24): 
            hourstring += '{:<3}'.format(n)
        graph.insert(0, hourstring)
        graph.insert(0, '='*72)

        # Find the max number of calls per hour in this day to determine the
        # number of rows we need.
        countmax = max(hours.iteritems(), key=operator.itemgetter(1))[1]
        for j in range(0, countmax):
            # Create a row of the graph.
            row = ''
            for k in range(0, 24):
                hours[k] = hours.get(k, 0)      # Add keys for 0-call hours

                # only print our symbol (+) if here at row n, there were at
                # least n calls at this hour
                if j < hours[k]: row += '+  '
                else: row += '   '
            graph.insert(0, row)

        # normalize the height, since we want visual continuity
        print '\n'*50
        for line in graph:
            print line

        raw_input("Press Enter to continue...") 
        os.system('clear')



if __name__ == '__main__':
    import argparse
    import textwrap
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            Parse a report file from IfByPhone with the following content:

            date_added
            dnis
            ani
            call_duration
            transfer_to_number
            phone_label
            '''))

    parser.add_argument('-a', '--agents', action='store_true',
            help='display missed calls by agent phone number')

    parser.add_argument('-c', '--callers', action='store_true',
            help='display each incoming caller with number of times called')

    parser.add_argument('-m', '--missed', action='store_true',
            help='display missed calls by date')

    parser.add_argument('-w', '--write', action='store_true',
            help='write input to new file')

    parser.add_argument('-b', '--byhour', action='store_true',
            help='display calls by hour and day')

    parser.add_argument('reportfile')

    args = parser.parse_args()

    theReport = csvtools.Report(args.reportfile)

    if args.missed:
        missed(theReport)
    elif args.callers:
        callers(theReport)
    elif args.agents:
        agents(theReport)
    elif args.byhour:
        byhour(theReport)
    elif args.write:
        theReport.write()
    else: print 'Run %s -h for usage' % (__file__)
