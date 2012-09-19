#!/usr/bin/python

def main():

    ##############
    #  Arg Prep  #
    ##############

    import callparser as cp
    import desklib.confidential as conf
    import csvtools
    import fetch_report
    import argparse
    import textwrap
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            Parse a report file from IfByPhone with the following content:

            date_added
            activity_info
            ani
            call_duration
            transfer_to_number
            '''))

    class ArgumentError(BaseException):
        pass

    ###############
    #  Arguments  #
    ###############

    # Determine input.
    parser.add_argument('-f', '--localfile',
            help='process a local report file (csv)')

    parser.add_argument('-d', '--date', nargs='+',
            help='download a report file between two dates '
                    'of format `yyyymmdd`')

    # Determine output.
    parser.add_argument('-c', '--callers', action='store_true',
            help='display each incoming caller with number of times called')

    parser.add_argument('-m', '--missed', action='store_true',
            help='display missed calls by date')

    parser.add_argument('-w', '--write', action='store_true',
            help='write input to new file')

    parser.add_argument('-a', '--agents', action='store_true',
            help='display missed calls by agent name and hour')

    parser.add_argument('-g', '--graphbyhour', action='store_true',
            help='graph calls by hour and day')

    args = parser.parse_args()

    ###########
    #  Logic  #
    ###########

    if args.date and args.localfile:
        raise ArgumentError('More than one input specified. '
                'Run callparser -h for usage')
    elif args.date:
        if len(args.date) > 2:
            raise ArgumentError('More than two dates specified. '
                    'You may only define a starting date and an ending date.')
        if len(args.date) == 1:
            args.date = args.date[0]
            args.date = cp.arg_hash.get(args.date, args.date)
            if type(args.date) == type(''):
                args.date = (args.date, args.date)

        (start, end) = args.date
        reportfile, res = fetch_report.downloadcsv(start, end, conf.apikey) 
    elif args.localfile:
        reportfile = args.localfile
    else:
        raise ArgumentError('No input specified. Run callparser -h for usage')

    theReport = csvtools.Report(reportfile)

    if args.missed:
        cp.missed(theReport)
    elif args.callers:
        cp.callers(theReport)
    elif args.agents:
        cp.byday(cp.timeparse(theReport), **cp.byagent())
    elif args.graphbyhour:
        cp.byday(cp.timeparse(theReport), **cp.byhour())
    elif args.write:
        cp.writeToJson(cp.timeparse(theReport))

    else:
        raise ArgumentError('No report type specified. '
                'Run callparser -h for usage')


if __name__ == '__main__':
    main()
