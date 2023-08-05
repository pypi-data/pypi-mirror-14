#!/usr/bin/env ipython

'''
This file has date & time utilities, especially in the context of quotes.
It can be used standalone or in conjunction with other modules for more
conveninet operations.

NOTE. any datetime object here (dtobj or date_obj) is of type dt.datetime.
That has a bunch of other properties if needed. Eg, to convert a dtobj
curr_datetime to a different timezone such as UTC:
    >> curr_datetime.astimezone(pytz.timezone('UTC'))
'''


import re
import datetime as dt
from datetime import date, timedelta
from pytz import timezone, all_timezones

#import time as t
#import dateutil as du
#import dateutil.parser as dp

import logging
logger = logging.getLogger()


_DAY_ = {6: 'sunday', 0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday',
            4: 'friday', 5: 'saturday'}

_MTH_ = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06',
         'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12' }


_DAY_BRIEF_ = {6: 'sun', 0: 'mon', 1: 'tue', 2: 'wed', 3: 'thu', 4: 'fri', 5: 'sat'}


#################################################################################
# Utility and help functions that could be imported by other modules
#################################################################################

def curr_time(loc=None):
    """Returns the current time in a specifc format:  day hr:min:sec, eg:

       If loc is not specified, localtime() is used, else one of various
       options for loc: [utc|eastern|pacific|central] entered as a string
       OR any valid timezone in pytz.all_timezones will do , eg: 'US/Mountain'

       print curr_time() -> 'Sun 16:26:20'
       print curr_time('US/Eastern) -> 'Sun 19:26:20'
       print curr_time('utc') -> 'Mon 00:26:20'         """

    # other ways to get time
    #   curr = t.localtime(t.time())
    #   t.asctime(t.gmtime()) for human version
    if loc == None: curr = dt.datetime.now()
    elif loc in all_timezones: curr = dt.datetime.now(loc)
    elif loc.lower() == 'utc':  curr = dt.datetime.now(timezone('UTC'))
    elif loc.lower() == 'eastern': curr = dt.datetime.now(timezone('US/Eastern'))
    elif loc.lower() == 'central': curr = dt.datetime.now(timezone('US/Central'))
    elif loc.lower() == 'pacific': curr = dt.datetime.now(timezone('US/Pacific'))
    else:
        logger.error('Unsupported location: {}'.format(loc))
        return 'Sun 00:00:00'

    return curr.strftime('%a %H:%M:%S')



def curr_date(loc=None):
    """Returns the current date. This is similar to curr_time and is timezone aware
    via loc. See the curr_time() function for description of loc.

    Returns a tuple of following form (2014, 11, 9, 'Sunday'). Note the lack of
    zero-padding"""

    if loc == None: curr = dt.datetime.now()
    elif loc in all_timezones: curr = dt.datetime.now(loc)
    elif loc.lower() == 'utc':  curr = dt.datetime.now(timezone('UTC'))
    elif loc.lower() == 'eastern': curr = dt.datetime.now(timezone('US/Eastern'))
    elif loc.lower() == 'central': curr = dt.datetime.now(timezone('US/Central'))
    elif loc.lower() == 'pacific': curr = dt.datetime.now(timezone('US/Pacific'))
    else:
        logger.error('Unsupported location: {}'.format(loc))
        return (0,0,0,'Sunday')

    return curr.year, curr.month, curr.day, curr.strftime('%A')



def curr_dt(loc=None):
    """Returns the current date&time as a datetime object. The calling API is similar to
    curr_time and is timezone aware via loc. See the curr_time() function for description
    of loc.

    HOWEVER, the return type is a dt.datetime tuple format w/timezone spec"""

    if loc == None: curr = dt.datetime.now()
    elif loc in all_timezones: curr = dt.datetime.now(loc)
    elif loc.lower() == 'utc':  curr = dt.datetime.now(timezone('UTC'))
    elif loc.lower() == 'eastern': curr = dt.datetime.now(timezone('US/Eastern'))
    elif loc.lower() == 'central': curr = dt.datetime.now(timezone('US/Central'))
    elif loc.lower() == 'pacific': curr = dt.datetime.now(timezone('US/Pacific'))
    else:
        logger.error('Unsupported location: {}'.format(loc))
        return dt.dateime(1900,1,1,tzinfo=timezone('UTC'))

    return curr



def first_of_month():
    """Gets the first of a month. This is NOT timezone aware""" #TODO.
    d = date.today()
    return date(d.year, d.month, 1)


def get_first_day(dtobj, d_years=0, d_months=0):
    """d_years, d_months are "deltas" to apply to dtobj"""
    y, m = dtobj.year + d_years, dtobj.month + d_months
    a, m = divmod(m-1, 12)
    return date(y+a, m+1, 1)


def get_last_day(dtobj):
    """Last day of month, given a date object"""
    return get_first_day(dtobj, 0, 1) + timedelta(-1)


def is_weekday(dtobj):
    """True if dtobj is not a Saturday or Sunday"""
    return dtobj.weekday() in range(0,4)


def is_weekend(dtobj):
    """True if dtobj is a Saturday or Sunday"""
    return dtobj.weekday() in (5,6)


def is_saturday(dtobj):
    """True if dtobj is a Saturday"""
    return dtobj.weekday() == 5


def is_sunday(dtobj):
    """True if dtobj is a Sunday"""
    return dtobj.weekday() == 6



def format_date( date_obj ):  # date_obj is a datetime.date object
    """Returns a formatted date string given a date object. If the day is
    the first of the month, then the day is dropped, eg:
        format_date ( datetime.date(2013, 04, 12)) returns 2013-04-12
        format_date ( datetime.date(2013,  4,  1)) returns 2013-04
    """
    if date_obj.day == 1:
        full_date = date_obj.isoformat()
        return full_date[0:7]
    else:
        return date_obj.isoformat()




def parse_date( adate ):
    """Returns a date object constructed by datetime(year, month, day) where
    year, month & day are parsed from informal input.
    Acceptable input will have one of two sequences(separated by '-' for '.')
        YYYY-MM-DD if ALL are numeric, or MM-DD-YY if alpha numeric eg:
        20140918    # must be 8 characters
        2014-09-18
        2014.9      # leading 0 is optional for month & day
        jul9.2014
        jul09.14    # leading prefix 20 is optional for year
        july-2014
        july-14     # This is confusing as hell though!! DO NOT USE
        9.18.14     # This is ambiguous...
        9/18/14     # This is ok
        09/18/2014  # This is ok
    """
    d = date.today()
    dflt_date = date(d.year, d.month, 1)   # pick 1st of month by default

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def get_md(monthday):   # return month, day tuple from a string
        if monthday.isalpha():  # we have month only
            day = 1
            mth_str = monthday[0:3].lower()
        else:           # both month and day are in here
            day = re.findall(r'\d+', monthday) [0]
            mth_str = re.split(r'\d+', monthday) [0]
            mth_str = mth_str[0:3].lower()

        try: month = _MTH_[mth_str]
        except KeyError, e:
            print "ERROR. Cannot find equivalent numeric for month", e
            month = date.today().month

        return int(month), int(day)

    def pad_year(yr):
        if   len(yr) == 1: return 2000 + int(yr) #    4 => 2004
        elif len(yr) == 2: return 2000 + int(yr) #   13 => 2013 scope for confusion 1913 or 2013?
        elif len(yr) == 3: return 2000 + int(yr) #  137 => 0    this is an error
        else:              return int(yr)        # 1995         cleanest
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    x = str(adate).lower().strip()

    if x.isdigit(): #* must be all numeric, eg: 20130412
        if len(x) == 8:
            fyear, fmonth, fday = int(x[0:4]), int(x[4:6]), int(x[6:8])
        else:
            print "ERROR. unmatched date format; needs to be 8 chars if specified this way", x
            return dflt_date

    else:           #* needs parsing

        if '/' in x: # slash '/' based is different from '-' or '.' based
            slash_based = True
            if '.' not in x and '-' not in x:
                y = re.split('/', x)
            else:
                print "ERROR. Cannot mix and match '/' with '.' , or '/' with '-'. "
                return dflt_date
        else:
            slash_based = False
            y = re.split('[-.]', x)

        digits = [0 if i.isdigit() else -1 for i in y]
        all_digits = True if sum(digits) == 0 else False


        if all_digits:  #** sequence must be year, month, day
            if len(y) == 3:
                if slash_based:
                    fyear, fmonth, fday = int(pad_year(y[2])), int(y[0]), int(y[1]) # eg, 5/18/13
                else:
                    fyear, fmonth, fday = int(y[0]), int(y[1]), int(y[2]) # eg, 2013-05-18
            elif len(y) == 2:
                if slash_based:
                    fyear, fmonth, fday = int(pad_year(y[1])), int(y[0]), 1 # eg, 5/13
                else:
                    fyear, fmonth, fday = int(y[0]), int(y[1]), 1 # eg, 2013-05

            elif len(y) < 2:
                print "ERROR. Not enough information to construct date. Passing default"
                return dflt_date
            else:
                print "WARNING. Ignoring info beyond given year, month, day"

        else:           #** sequence must be month, day, year
            if slash_based:
                print 'ERROR. A "/" based date must consist ONLY of digits in month/day/year format'
                return dflt_date
            if len(y) == 3:  # eg, jan-14.2013  or may.25.15, etc
                fyear = pad_year(y[2])
                fmonth, fday = get_md( y[0]+y[1] )
            elif len(y) == 2:  # eg, jan.14 or jan3-14
                fyear = pad_year(y[1])
                fmonth, fday = get_md( y[0] )
            elif len(y) == 1:
                print "ERROR. Not enough information to construct date. Passing default"
                return dflt_date
            else:
                print "WARNING. Ignoring info beyond given month, day, year"

    # finally we got this far...
    try: date_obj = date(fyear, fmonth, fday)
    except Exception, e:
        print "ERROR. ", e
        return dflt_date

    return date_obj



def markets_open():
    """Return True if markets are open. Uses the NYC/Eastern time to figure this out"""

    wallst_time = dt.datetime.now(timezone('US/Eastern'))
    chour  =  wallst_time.hour
    cminute =  wallst_time.minute
    cweekday =  wallst_time.weekday()
    chour_frac  =  chour + cminute/60.0

    closed = (cweekday in (5,6)) or (chour_frac < 6.5) or (chour > 13)
    return False if closed else True



def markets_closed():
    """Return True if markets are closed"""
    return not markets_open()



def exact_exp_date(results, exp):
    """Returns a string of unique expiry date in yyyy-mm-dd form
    results: tuple of (Ticker[0] Strike[1] Type[2] Expiration[3] Last[4] Bid[5] Ask[6])
        exp: expiration date that was entered or inferred. however, may not have
             day of the month, or may resolve to multiple dates."""
    exp_dates = set([])
    for result in results[1:]:
        exp_dates.add(result[3])

    if len(exp_dates) == 0:
        print "WARNING. No matching date found! Try again."

    if len(exp_dates) != 1:
        print "WARNING. multiple dates found! "
        for d in exp_dates: print "  ->   ", d
        print "Try again with exact one."
    exp_date = ' '.join(list(exp_dates))
    return exp_date


def iso_date(adate):
    """Returns True if adate is in form of 'yyyy-dd-mm' else False"""
    if type(adate) != str or len(str(adate)) !=10 : return False
    alist = adate.split('-')
    if len(alist) != 3: return False

    y,m,d = alist
    if y.isdigit() and len(y) == 4 and \
       m.isdigit() and len(m) == 2 and \
       d.isdigit() and len(d) == 2: return True
    else: return False


def iso_date2(adate):
    """Returns int tuple (yyyy,mm,dd) if adate is in form of 'yyyy-dd-mm' else (0,0,0)"""
    if type(adate) != str or len(str(adate)) !=10 : return (0,0,0)
    alist = adate.split('-')
    if len(alist) != 3: return  (0,0,0)

    y,m,d = alist
    if y.isdigit() and len(y) == 4 and \
       m.isdigit() and len(m) == 2 and \
       d.isdigit() and len(d) == 2: return (int(y), int(m), int(d))
    else: return (0,0,0)




#################################################################################
# Old functions kept for reference - TEMPORARILY
#################################################################################
# def curr_date_old():    #TODO. make this obsolete
#     curr   = t.localtime(t.time())
#     wday   = _DAY_[curr.tm_wday] # week day
#     day    = curr.tm_mday         # day of month
#     year   = int(curr.tm_year)
#     month  = curr.tm_mon
#     print "types", type(year), type(month), type(day), type(wday)  # 2013, 04, 12, friday
#     return year, month, day, wday  # 2013, 04, 12, friday
#
#
# def markets_open_old():
#     """Return True if markets are open. Uses naive time"""
#
#     curr = t.localtime(t.time())
#     curr_hour = float(curr.tm_hour) + float(curr.tm_min)/60.0
#     time_str = str(curr.tm_hour) + ':' + str(curr.tm_min) + ':' + str(curr.tm_sec)
#     ## # print 'current weekday and time', _DAY_[curr.tm_wday], time_str    # DEBUG
#
#     # After 1 pm or before 6:30 am, markets are closed
#     closed = curr_hour > 13.0 or curr_hour < 6.5 or \
#         _DAY_[curr.tm_wday] == 'Saturday' or _DAY_[curr.tm_wday] == 'Sunday'
#
#     return False if closed else True
#
#
# def new_parse_date( adate ):    # TODO. Is this better than the existing one?
#     # return du.parser.parse(adate)
#     # print '-- adate = ', adate, '--'  // has bugs, eg, may23.12 becomes 05/23/2014
#     return dp.parse(adate).date()




# *********************************************************
# Main Routine (& test functions)
# *********************************************************
def test_timeutils(args):
    print 'Curr time:' , curr_time()
    print 'Curr date:' , curr_date()
    print format_date( date(2013, 04, 12) )
    print format_date( date(2013, 04, 1) )
    print "Market open  ? ", markets_open()
    print "Market closed? ", markets_closed()
    print 'GOOD DATES\n', "***********"
    print 1, parse_date('jul23.14')
    print 2, parse_date('20140918')
    print 3, parse_date('2014-09-18')
    print 4, parse_date('2014.9')
    print 5, parse_date('jul9.2014')
    print 6, parse_date('jul09.14')
    print 7, parse_date('july-2014')
    print 8, parse_date('july-14')
    print 'BAD DATES\n', "***********"
    print 1, parse_date('2014091')
    print 2, parse_date('113-13-59')
    print 3, parse_date('01131359')
    print 4, parse_date('jux.14')


if __name__ == '__main__':
    import sys
    test_timeutils(sys.argv[1:])
