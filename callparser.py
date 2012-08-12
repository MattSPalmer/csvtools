#!/usr/bin/env python

import csvtools
import typeutil
import operator
import json
import os

from collections import Counter
from confidential import agentKeys
from datetime import datetime

class AutoVivification(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

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

def timeparse(calls):
    # Isolate date strings and convert to date format from string, ignoring the
    # header row when iterating over calls
    def toDate(datestr):
        return datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S")

    calls.removeColumns("dnis","ani","call_duration","phone_label")
    for call in calls[1:]:
        call[0] = toDate(call[0])

    # Hash the hours of each call to the day of each call.
    timestruct = AutoVivification()
    for call in calls[1:]:
        (year, month, day, hour) = (call[0].year,
                call[0].month, call[0].day, call[0].hour)
        timestruct[year][month][day][hour] = timestruct[year][month][day].get(
                hour, [])
        timestruct[year][month][day][hour].append(call[1] != '')
    return timestruct

def drawgraph(period):
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

    # Creating and drawing the graph for each day (key) and set of hour counts (values)
    for year, months in sorted(period.iteritems()):
        for month, days in sorted(months.iteritems()):
            for day, hours in sorted(days.iteritems()):

                graph = []

                # What day are we looking at?
                graph.insert(0, '{0} {1}, {2}\n'.format(monthhash[month], day,
                    year))

                # Each row is an hour of the day
                for n in range(0, 24): 
                    hours[n] = hours.get(n, [])      # Add keys for 0-call hours
                    hourstring = ''
                    hourstring += '{:<3}|'.format(n)

                    # Using the truth state of each list item in the value of an hour's
                    # key, print one symbol for calls taken and another for missed.
                    for state in hours[n]:
                        symbol = '+' if state else 'o'
                        hourstring += '{:<3}'.format(symbol)
                    graph.insert(0, hourstring)

                # Normalize the height, since we want visual continuity
                print '\n'*50
                for line in reversed(graph):
                    print line

                raw_input("Press Enter to continue...") 
                os.system('clear')

    drawgraph(timeparse(calls))

def writeToJson(daydata, dataname='data'):
    dataname += '.json'
    f = open(dataname, 'wb')
    f.write(json.dumps(daydata))
    f.close()




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

    parser.add_argument('-g', '--graphbyhour', action='store_true',
            help='graph calls by hour and day')

    parser.add_argument('-t', '--test', action='store_true',
            help='testing stuff')

    parser.add_argument('reportfile')

    args = parser.parse_args()

    theReport = csvtools.Report(args.reportfile)

    if args.missed:
        missed(theReport)
    elif args.callers:
        callers(theReport)
    elif args.agents:
        agents(theReport)
    elif args.graphbyhour:
        drawgraph(timeparse(theReport))
    elif args.write:
        writeToJson(timeparse(theReport))
    elif args.test:
        print timeparse(theReport)
    else: print 'Run %s -h for usage' % (__file__)
