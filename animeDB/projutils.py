#!/usr/bin/python

import datetime

def format_datetime(dtime_obj):
    
    y = str(dtime_obj.year)
    m = str(dtime_obj.month)
    d = str(dtime_obj.day)

    h = str(dtime_obj.hour)
    mi = str(dtime_obj.minute)
    s = str(dtime_obj.second)

    dtime_string_f = y + "-" + m + "-" + d + " " + h +":"+mi+":"+s

    return dtime_string_f

    return -1

