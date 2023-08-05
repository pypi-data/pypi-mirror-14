# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 10:31:00 2016

@author: roel
"""
from opengrid import ureg, Q_
import pandas as pd
from dateutil import rrule
import datetime as dt


def parse_date(d):
    """
    Return a pandas.Timestamp if possible.  
    
    Parameters
    ----------
    d : Datetime, float, int, string or pandas Timestamp
        Anything that can be parsed into a pandas.Timestamp
        
    Returns
    -------
    pts : pandas.Timestamp
    
    Raises
    ------
    ValueError if it was not possible to create a pandas.Timestamp
    """
    
    if isinstance(d, float) or isinstance(d, int):
        # we have a POSIX timestamp IN SECONDS.
        pts = pd.Timestamp(d, unit='s')
        return pts
        
    try:
        pts = pd.Timestamp(d)
    except:
        raise ValueError("{} cannot be parsed into a pandas.Timestamp".format(d))
    else:
        return pts


def time_to_timedelta(t):
    """
    Return a pandas Timedelta from a time object

    Parameters
    ----------
    t : datetime.time

    Returns
    -------
    pd.Timedelta

    Notes
    ------
    The timezone of t (if present) is ignored.
    """
    return pd.Timedelta(seconds=t.hour*3600+t.minute*60+t.second+t.microsecond*1e-3)


def split_by_day(df, starttime=dt.time.min, endtime=dt.time.max):
    """
    Return a list with dataframes, one for each day

    Parameters
    ----------
    df : pandas DataFrame with datetimeindex
    starttime, endtime :datetime.time objects
        For each day, only return a dataframe between starttime and endtime
        If None, use begin of day/end of day respectively

    Returns
    -------
    list, one dataframe per day.
    """
    if df.empty:
        return None

    df = df[(df.index.time >= starttime) & (df.index.time < endtime)]  # slice between starttime and endtime
    list_df = [group[1] for group in df.groupby(df.index.date)]  # group by date and create list
    return list_df

def unit_conversion_factor(source, target):
    """
    Shorthand function to get a conversion factor for unit conversion.

    Parameters
    ----------
    source, target : str
        Unit as string, should be parsable by pint

    Returns
    -------
    cf : float
        Conversion factor. Multiply the source value with this factor to
        get the target value.  Works only for factorial conversion!

    """

    return 1*ureg(source).to(target).magnitude


def dayset(start, end):
    """
        Takes a start and end date and returns a set containing all dates between start and end

        Parameters
        ----------
        start : datetime-like object
        end : datetime-like object

        Returns
        -------
        set of datetime objects
    """

    res = []
    for dt in rrule.rrule(rrule.DAILY, dtstart=start, until=end):
        res.append(dt)
    return sorted(set(res))