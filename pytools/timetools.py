# -*- coding: utf-8 -*-

"""
This module provides a list of tool functions about date/time.
- diff_time
- str_to_date

Author : Eric OLLIVIER
"""

import time
import datetime as dt

# =============================================================================
# str_to_date
# =============================================================================
def str_to_date(s_date, sep='/', format='DMY'):
    """
    Convert a date with 'str' type to date object (from datetime module).
    - s_date: string contains the date
    - sep : the separator between the date items. By default the value is '/'
    - format : define the order of the item
        'Y' for year, 'M' for month, 'D' for day.
        example : the format 'DMY' defines a date like '01/08/1972'
    """
    try:
        idx_format = list(format.upper())
        idx_date = s_date.split(sep)
        return dt.date(int(idx_date[idx_format.index('Y')]),
                       int(idx_date[idx_format.index('M')]),
                       int(idx_date[idx_format.index('D')]))
    except:
        return None
    
# =============================================================================
# diff_times
# =============================================================================
def diff_times(date1, date2, unit='second'):
    """
    This function return the differential time between two dates or times.
    'date1' and 'date2' must be the same type and among the following type : 
        date type = {datetime, date, time}
        
    The return value is a float type exprimed in the unit passed in parameters.
    The unit can take the following value : 
        unit type = {'day', 'hour', 'minute', 'second'}
    """
    # Parameters checking
    if not isinstance(date1, (dt.datetime, dt.date, dt.time)):
        raise TypeError(type(date1))
        return None
    
    if not isinstance(date2, (dt.datetime, dt.date, dt.time)):
        raise TypeError(type(date2))
        return None

    if type(date1) != type(date2): # Check the same type
        raise TypeError(type(date1), type(date2))
        return None
    
    # Set the order of date
    if date1 > date2:
        date_min = date2
        date_max = date1
    else:
        date_min = date1
        date_max = date2
    
    # Convertion to second unit
    _date_min = 0 
    _date_max = 0
    if isinstance(date_max, (dt.time)):
        _date_min = date_min.second + date_min.minute*60 + date_min.hour*3600
        _date_max = date_max.second + date_max.minute*60 + date_max.hour*3600
    _date_diff = _date_max-_date_min
           
    if isinstance(date1, (dt.date, dt.datetime)):
        _delta_date = date_max - date_min
        _date_diff = _delta_date.total_seconds()
    
    # Convertion to target unit
    if unit == 'second':
        return _date_diff
    elif unit == 'minute':
        return _date_diff/60
    elif unit == 'hour':
        return _date_diff/3600
    elif unit == 'day':
        return _date_diff/(24*3600)
    
# end of file : timetools.py
