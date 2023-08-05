#!/usr/bin/python

# ###############################
#
# timefunc.py 0.7
# Code made by bgo@vedur.is
# Iceland Met Office
# 2015
#
# ###############################

"""

In this program are the following functions in order:


TimetoYearf(year, month, day, hour=12, minute=0, sec=0):
TimefromYearf(yearf, string=None):
currDatetime(days=0,refday=datetime.datetime.today(),string=None):
currDate(days=0,refday=datetime.datetime.today(),string=None,fromYearf=False):
gpsWeekDay( days=0, refday=currDate() , fromYearf=False):
currTime(string):
DayofYear(days=0, year=None, month=None, day=None):
DaysinYear( year=None ):
yearDoy(yearf):
currYearfDate( days=0, refday=datetime.date.today(), fromYearf=True ):
currYear():
shlyear(yyyy=currYear(),change=True):
dateTuple(days=0,refday=datetime.datetime.today(),string=None,fromYearf=False):
datefgpsWeekDOW(gpsWeek,DOW,string=None,leapSecs=16):
datefgpsWeekDoy(gpsWeek,Doy,string=None,leapSecs=16):
toDatetime(dStr,fStr):
_to_ordinalf(dt):

"""


import time, math, calendar, datetime, pytz
import numpy as np


#importing constants from gpstime.
from gtimes.gpstime import secsInWeek, secsInDay, gpsEpoch, gpsFromUTC, UTCFromGps
from dateutil.tz import tzlocal


# Core functions ---------------------------

def TimetoYearf(year, month, day, hour=12, minute=0, sec=0):
    """
    converts time cal+time of day into fractional year.
    input:
        date: as year, month, day
        time: as hour, minute, sec (defaults to the middle of the day at 12 am) 
    output:
        returns fractional year

    """
    doy = DayofYear(0,year, month, day)-1
    secofyear=doy*secsInDay + ( hour*60+minute )*60 + sec

    daysinyear=DaysinYear(year)
    secinyear=daysinyear*secsInDay

    yearf = year+secofyear/float(secinyear)
    
    return yearf

def TimefromYearf(yearf, string=None):
    """ 
    Returns a date and/or time according to a formated string derived from a fractional year. 
    Intended to manipulate time format of gamit time series files which is in fractional years.
    Input: 
        string: 
            formated according to format codes that the C standard (1989 version) see documentation for 
            datetime module. Example "%Y %m %d %H:%M:%S %f"
        year: fractional year. example 2012.55
        
    Output: Returns time of the input year formated according to input string.
    """
    # to integer year
    year = int(math.floor(yearf))

    # converting to doy, hour, min, sec, microsec 
    daysinyear = DaysinYear(year)
    dayf = (yearf-year)*daysinyear+1
    doy = int(math.floor(dayf)) # day of year)
    fofday = dayf-doy
    Hour = int(math.floor( (fofday)*24)) # hour of day
    Min  = int(math.floor( (fofday)*24*60 % 60)) # minute of hour
    fsec = fofday*24*60*60 % 60
    Sec  = int(math.floor(fsec)) # second of minute 
    musec = int(math.floor((fsec-Sec)*1000000)) # microsecond 0 - 1000000

    timestr = "%d %.3d %.2d:%.2d:%.2d %s" % (year,doy,Hour,Min,Sec,musec)
    dt = datetime.datetime.strptime( timestr , "%Y %j %H:%M:%S %f") # Create datetime object from timestr
    if string:
        if string == "ordinalf": # return a floating point ordinal day
            return dt.toordinal()+fofday
        else:
            return dt.strftime(string)
    else: # just return the datetime instanse
        return dt

def currDatetime(days=0,refday=datetime.datetime.today(),string=None):
    """
    Returns a datetime object for the date, "days" from refday.

    Input:
        days: integer, Defaults to 0
              days to offset
        refday: datetime object or a string, defaults to datetime.datetime.today()
              reference day 
        string: formating string. defaults to None (infering refday as datetime object)
              If refday is a date string, this has to contain it's formating (i.e %Y-%m-%d %H:%M)

    Output:
        returns a datetime object

         defaults to current day if ran without arguments
    """
    day = refday + datetime.timedelta(days)
    if string:
        return day.strftime(string)
    else:
        return day

def currDate(days=0,refday=datetime.date.today(),string=None,fromYearf=False):
    """
    Returns a datetime object for the date, "days" from today.
    Defaults to current day
    """
    
    if fromYearf and type(refday) == float or type(refday) == int:
        refday = TimefromYearf(refday)

    day = refday + datetime.timedelta(days)
    if string == "yearf":
        return TimetoYearf(*day.timetuple()[0:3])
    elif string:
        return day.strftime(string)
    else:
        return day

def gpsWeekDay( days=0, refday=currDate() , fromYearf=False):
    """
    Returns tuple gps Week and day of Week
    """
    if fromYearf:
        print refday
        refday = TimefromYearf(refday,)
        print refday

    refday = refday + datetime.timedelta(days)
    tmp = refday.timetuple()[0:3]

    return gpsFromUTC(*tmp,hour=12,min=0,sec=0)[0:3:2]



############################################
# derived functions

def currTime(string):
    """
    Returns the current UTC time in a format determent by string

    input:
        string: A string determinaning the outpur format of the current time
                formated according to format codes that the C standard (1989 version) requires, 
                see documentation for datetime module. Example
                Example,  string = "%Y %j %H:%M:%S %f" -> '2013 060 16:03:54 970424'
                See datetime documentation for details

    output: 
                Returns the current time formated according to input string.

    """

    return datetime.datetime.now(tzlocal()).strftime(string)

def DayofYear(days=0, year=None, month=None, day=None):
    """
    Returns the day of year, "days" (defaults to 0) relative to the date given 
    i.e. (year,month,day) (defaults to today)
    No argument returns the day of today
    
    input:
        days: Day relative to (year,month,day) or today if (year,month,day) not given
        year: Four digit year "yyyy". Example 2013  
        month: Month in integer from 1-12
        day: Day of month as integer 1-(28-31) depending on month
    output:
        doy: Integer containing day of year. Exampls (2013,1,3) -> 60
                spans 1 -365(366 if leap year)
    """

    if year and month and day:
        nday = datetime.date(year,month,day)+datetime.timedelta(days)
        doy = nday.timetuple()[7]
    else:
        nday = datetime.date.today() + datetime.timedelta(days)
        doy = nday.timetuple()[7]

    return doy

def DaysinYear( year=None ):
    """
    Returns the last day of year 365 or 366, (defaults to current year)
    
    input:
        year: Integer or floating point year (defaults to current year)
    out:
        daysinyear: Returns and integer value, the last day of the year  365 or 366
    """

    if year == None: # defaults to current year
        year=datetime.date.today().year
    
    year = np.int_(np.floor(year)) # allow for floating point year
    daysinyear =  366 if calendar.isleap(year) else 365   #checking if it is leap year and assigning the correct day number
    
    return daysinyear

def yearDoy(yearf):
    """
    simple wrapper that calls TimefromYearf, to return a date in the form "year-doyT" from fractional year.
    convinient for fancy time labels in GMT hence the T.
    """
    return TimefromYearf(yearf,"%Y-%jT",)

def currYearfDate( days=0, refday=datetime.date.today(), fromYearf=True ):
    """
    Wrapper for currDate() to return the date, "days" from "refday"  
    in decimal year, defaults to current day
    """

    return currDate(days=days,refday=refday,string="yearf",fromYearf=fromYearf)
    
def currYear():
    """
    Current year in YYYY
    """
    return datetime.date.today().year


def shlyear(yyyy=currYear(),change=True):
    """
    Changes a year from two digit format to four and wize versa.
    input:  
        YYYY: Year in YYYY or YY (defaults to current year)
        change: True of False convinies in case we want to pass YYYY unchanged through the function

    output: Year converterded from two->four or four->two digit form.
    returns current year in two digit form in the apsence of input
    """
    if len(str(abs(yyyy))) == 4 and change == True:
        yyyy = datetime.datetime.strptime(str(yyyy),"%Y")
        return yyyy.strftime("%y")
    elif len(str(abs(yyyy))) <= 2 and change == True:
        yyyy = datetime.datetime.strptime("%02d" % yyyy,"%y")
        return yyyy.strftime("%Y") 
    elif change == False:
        return yyyy

def dateTuple(days=0,refday=datetime.datetime.today(),string=None,fromYearf=False):
    """
    Return tuple with different elements of a given date
    (year, month, day of month, day of year, fractional year, gps week, gps day of week)
    """

    #(Week,dow) = gpsWeekDay(days,refday,fromYearf)
    day=currDatetime(days,refday,None)
    month=day.strftime("%b")
    day=day.timetuple()
    return day[0:3] + day[7:8] + (currYearfDate(days,refday),) + gpsWeekDay(days,refday,fromYearf) + (int(str(day[0])[-1]),) + (int(shlyear(day[0])),) + (month,)


# Temporary functions to deal with numpy arrays Will become apsolete when implementd directly in the main moduvls

def convfromYearf(yearf, string=None):
    # from floating point year to floating point ordinal

    import numpy as np
    
    tmp = range(len(yearf))

    for i in range(len(yearf)):
        if string:
            tmp[i] = TimefromYearf(yearf[i],string)
        else:
            tmp[i] = (TimefromYearf(yearf[i]))

    return np.asarray(tmp)


# functions using gps week and day of week ----------------

def datefgpsWeekDOW(gpsWeek,DOW,string=None,leapSecs=16):
    """
    Return date converted from GPS Week and Day of week 
    """
    
    SOW = (DOW+1) * secsInDay
    day=datetime.datetime(*UTCFromGps(gpsWeek, SOW,leapSecs=leapSecs)[0:3])

    if string == "yearf":
        return TimetoYearf(*day.timetuple()[0:3])
    elif string == "tuple":
        return day.timetuple()[0:3]
    elif string:
        return day.strftime(string)
    else:
        return day 

def datefgpsWeekDoy(gpsWeek,Doy,string=None,leapSecs=16):
    """
    Return date converted from GPS Week and Day of year 
    """
    SOW = 1 * secsInDay
    day=datetime.datetimes(*UTCFromGps(gpsWeek, SOW,leapSecs=leapSecs)[0:3])
    doy0 = day.timetuple()[7] 
    if doy0 <= Doy < doy0 + 7:
        DOW = Doy - doy0
        day = day + datetime.timedelta(DOW)
    else: 
        print "ERROR: Doy %s not in week %s returning date of day 0 in week %s" % (Doy, gpsWeek, gpsWeek)

    if string == "yearf":
        return TimetoYearf(*day.timetuple()[0:3])
    elif string == "tuple":
        return day.timetuple()[0:3]
    elif string:
        return day.strftime(string)
    else:
        return day 

def toDatetime(dStr,fStr):
    """
    Convert date/time strings to datetime objects accorting to formating rule defined in fStr
    
    input:
        
        dStr: (list of) string(s)  holding a date and/or time 

        fStr: formating rule constituding the  following input formats 
            default: fStr formated according to standard rules see for example datetime documentation for formating (i.e dStr=20150120 entailes fStr=%Y%m%d )
            yearf: decimal year 
            w-dow: GPS week and day of week on the form WWWW-DOW (example 1820-3, where DOW is sunday = 0 ... 6 = saturday)
            w-doy: GPS week and day of year on the form WWWW-DOY
            
    output:
        returns datetime object.

    """

    if type(dStr) == datetime.datetime: 
        day=dStr

    elif fStr == "yearf":
        day=TimefromYearf(float(dStr))

    elif fStr == "w-dow":
        wdow=tuple([int(i) for i in dStr.split("-")])
        day=timefunc.datefgpsWeekDOW(*wdow)

    elif fStr == "w-doy":
        wdoy=tuple([int(i) for i in dStr.split("-")])
        day=timefunc.datefgpsWeekDoy(*wdoy)
    else:
        day=datetime.datetime.strptime(dStr,fStr)

    #returning datetime object
    return day

def toDatetimel(dStrlist,fStr):
    """
    A simple wrapper around toDatetime to allow for list input works like toDatetime if dStrlist is a single object.
    
    input:
        
        dStr: (list of) string(s)  holding a date and/or time 

        fStr: See docstring of toDatetime

    output:
        returns a list of datetime objects.

    """
    
    # To allow for single object input as well, otherwise python will treat a string as a list in the for loop
    if type(dStrlist) is not list:
        dStrlist = [ dStrlist ]

    dStrlist = [  toDatetime(dStr,fStr) for dStr in dStrlist ] # converting to a list of datetime strings
        
    if len(dStrlist) == 1: # toDatetime can be replaced by toDatetime
        return dStrlist[0]
    else:
        return dStrlist



HOURS_PER_DAY = 24.
MINUTES_PER_DAY  = 60.*HOURS_PER_DAY
SECONDS_PER_DAY =  60.*MINUTES_PER_DAY
MUSECONDS_PER_DAY = 1e6*SECONDS_PER_DAY
SEC_PER_MIN = 60
SEC_PER_HOUR = 3600
SEC_PER_DAY = SEC_PER_HOUR * 24
SEC_PER_WEEK = SEC_PER_DAY * 7



def _to_ordinalf(dt):
    """
    Convert :mod:`datetime` to the Gregorian date as UTC float days,
    preserving hours, minutes, seconds and microseconds.  Return value
    is a :func:`float`.
    """

    if hasattr(dt, 'tzinfo') and dt.tzinfo is not None:
        delta = dt.tzinfo.utcoffset(dt)
        if delta is not None:
            dt -= delta

    base =  float(dt.toordinal())
    if hasattr(dt, 'hour'):
        base += (dt.hour/HOURS_PER_DAY + dt.minute/MINUTES_PER_DAY +
                 dt.second/SECONDS_PER_DAY + dt.microsecond/MUSECONDS_PER_DAY
                 )
    return base

