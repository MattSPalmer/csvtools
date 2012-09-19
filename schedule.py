import shiftplanning.shift_planning as sp
from desklib.confidential import sp_creds
from desklib.classes import DeskObject


s = sp.ShiftPlanning(sp_creds['key'], sp_creds['username'],
        sp_creds['password'])
s.do_login()


s.get_schedules()
s.create_shift(
        {
            'start_time': '10:00 am',
            'end_time': '11:00 pm',
            'start_date': '10 November 2012',
            'end_date': '10 November 2012',
            'schedule': '82020'
            }
        )

s.get_shifts()

print s.get_public_data()
