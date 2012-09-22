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

connection = sp.ShiftPlanning(sp_creds['key'],
sp_creds['username'], sp_creds['password'])

connection.do_login()

def onNow(daydiff=0):
    now = dt.datetime.now() + dt.timedelta(days=daydiff)
    connection.get_shifts(now, now, mode='overview')
    shifts = map(AttributeRich, connection.get_public_data())
    employees = []
    for shift in shifts:
        if shift.start < now < shift.end:
            employees += [e.name for e in shift.employees]
    return employees

print onNow()

connection.do_logout()

