#!/usr/bin/env python

import desklib.confidential as conf
import datetime as dt
import json

from calendar    import month_name, day_name, weekday

agent_keys = conf.agent_keys
sales      = conf.sales
today = dt.datetime.today()
yesterday = today + dt.timedelta(days=-1)

#############
#  Classes  #
#############

class AutoVivification(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

################
#  Date Tools  #
################

def dtToYMD(datetime):
    return datetime.date().strftime('%Y%m%d')

def timeRange(start_dt=None, end_dt=today, delta=None):
    if start_dt == None and delta == None:
        raise NameError('Remember to specify either start_dt or delta.')
    elif not start_dt:
        start_dt = end_dt + dt.timedelta(days=delta)
    return (dtToYMD(start_dt), dtToYMD(end_dt))

arg_hash = {
        'today': timeRange(delta=0),
        'yesterday': timeRange(start_dt=yesterday, end_dt=yesterday),
        'week': timeRange(delta=-7),
        'month': timeRange(delta=-30)
        }

#######################
#  Parsing Functions  #
#######################

def timeparse(calls):
    # Isolate date strings and convert to date format from string, ignoring the
    # header row when iterating over calls
    def toDate(datestr):
        return dt.datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S")
    calls.filter('activity_info', query='Customer Care')
    calls.removeColumns("activity_info", "ani", "call_duration")
    for call in calls[1:]:
        call[0] = toDate(call[0])

    # Hash the hours of each call to the day of each call.
    timestruct = AutoVivification()
    for call in calls[1:]:
        (year, month, day, hour) = (call[0].year,
                call[0].month, call[0].day, call[0].hour)
        timestruct[year][month][day][hour] = timestruct[year][month][day].get(
                hour, [])
        timestruct[year][month][day][hour].append(call[1])
    return timestruct

######################
#  Output Functions  #
######################

def drawgraph(**kwargs):
    title = kwargs['title']
    datagen = kwargs['datagen']
    data = kwargs.get('data', None)
    axis = kwargs['axis']

    graph = []


    graph.append('\n\n')
    graph.append(title)
    graph.append('-'*len(title))

    for row in axis:
        rowstring = []
        padding = len(str(max(axis)))

        rowstring.append('{0:>{1}}| '.format(row, padding))

        for n in datagen(row,data):
            rowstring.append('{:<2}'.format(n))

        graph.append(''.join(rowstring))
    for row in graph:
        print row

def writeToJson(daydata, dataname='data'):
    dataname += '.json'
    f = open(dataname, 'wb')
    f.write(json.dumps(daydata))
    f.close()

########################
#  Data Organizations  #
########################

def byday(datagroup, **opts):
    prefunc = opts['prefunc']
    iterfunc = opts['iterfunc']

    params = dict(datagen=prefunc())

    for year, months in sorted(datagroup.iteritems()):
        for month, days in sorted(months.iteritems()):
            for day, hours in sorted(days.iteritems()):

                params = iterfunc(params, year, month, day, hours)
                
                drawgraph(**params)

                if len(months) > 1 or len(days) > 1:
                    raw_input('Press Enter to continue...')

def byhour():
    def prefunc():
        def generator(row, data):
            for call in data[row]:
                if agent_keys.get(call, '') not in sales:
                    if call:
                        yield agent_keys.get(call, '+')[0]
                    else:
                        yield '-'
        return generator


    def iterfunc(params, year, month, day, hours):
        dayOfWeek = day_name[weekday(year, month, day)]

        params['title'] = '{0} {1} {2}, {3}'.format(dayOfWeek,
                month_name[month], day, year)
        params['axis'] = [n for n in range(7, 22)]
        params['data'] = hours
        return params
    
    return {'prefunc': prefunc, 'iterfunc': iterfunc}

def byagent():
    def prefunc():
        def generator(row, data):
            for call in data:
                if agent_keys.get(call, '') == row:
                    yield '+'
        return generator

    def iterfunc(params, year, month, day, hours):
        dayOfWeek = day_name[weekday(year, month, day)]
        agents = list(set(agent_keys.values()))
        incoming = reduce(lambda x, y: x+y, hours.values())

        params['title'] = '{0} {1} {2}, {3}'.format(dayOfWeek,
                month_name[month], day, year)
        params['axis'] = agents
        params['data'] = incoming
        return params
    
    return {'prefunc': prefunc, 'iterfunc': iterfunc}

def main():
    pass

if __name__ == '__main__':
    main()
