#!/usr/bin/env python

import csvtools
import typeutil
from collections import Counter
from confidential import agentKeys


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
    breakdown = calls.filter('transfer_to_number', '', inverse=True)
    incoming = dict(Counter(breakdown.toDict()['ani']))
    for k, v in incoming.iteritems():
        print k, v

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

    parser.add_argument('reportfile')

    args = parser.parse_args()

    theReport = csvtools.Report(args.reportfile)

    if args.missed: missed(theReport)
    elif args.callers: callers(theReport)
    elif args.agents: agents(theReport)
    elif args.write: theReport.write()
    else: print 'Run %s -h for usage' % (__file__)
