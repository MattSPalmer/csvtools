from datetime import datetime

def is_num(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def to_num(s):
    if is_num(s):
        return float(s)
    else:
        return(s)

def formatPhoneNum(number):
    """Prettify a string containing the digits of a phone number. If string is
    empty, return 'Missed'. If string is not 10 digits, do nothing."""
    if len(number) == 10:
        return "(%s) %s-%s" % (number[:3], number[3:6], number[6:])
    elif len(number) == 0:
        return 'Missed'
    else: return number

def days(datelist):
    """Given a list of dates of the form '' """
    uniqdays = {}
    for date in datelist:
        monthAndDay = (date.month, date.day)
        if monthAndDay not in uniqdays:
            uniqdays[monthAndDay] = 1
        else:
            uniqdays[monthAndDay] += 1
    return uniqdays
