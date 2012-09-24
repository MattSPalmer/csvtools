import shiftplanning as sp
import datetime as dt
from desklib.confidential import sp_creds

class AttributeRich(object):
    def __init__(self, data, pref_attrs={}):
        self.data = data
        pref_attrs = {
                "start_timestamp": "start",
                "end_timestamp": "end"
                }
        for k, v in self.data.iteritems():
            k = pref_attrs.get(k, k)
            try:
                v = dt.datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
            except:
                pass
            try:
                v = map(AttributeRich, v)
            except:
                pass
            try:
                setattr(self, k, AttributeRich(v))
            except:
                setattr(self, k, v)

    def __repr__(self):
        return str(self.data)


def get_shifts(start, end):
    connection = sp.ShiftPlanning(sp_creds['key'], sp_creds['username'],
            sp_creds['password'])
    connection.do_login()
    connection.get_shifts(start, end, mode='overview')
    shifts = map(AttributeRich, connection.get_public_data())
    connection.do_logout()
    del connection
    return shifts

def onNow():
    now = dt.datetime.now()
    shifts = get_shifts(now, now)
    employees = []
    for shift in shifts:
        if shift.start < now < shift.end:
            employees += [e.name for e in shift.employees]

    return employees

def onDay(num, hours=False):
    date = dt.datetime.now() + dt.timedelta(days=num)
    shifts = get_shifts(date, date)
    employees = []
    if hours == True:
        for shift in shifts:
            sched_str = "{} - {}".format(
                    shift.start.strftime('%H:%M'),
                    shift.end.strftime('%H:%M')
                    )
            delta = shift.end - shift.start
            delta_hours = delta.days*24 + delta.seconds/3600
            employees += [(e.name, sched_str, delta_hours) for e in shift.employees]
    else:
        for shift in shifts:
            employees += [e.name for e in shift.employees]

    return employees

def isWorking(name):
    return name in onNow()

