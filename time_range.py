from __future__ import absolute_import

import re
import time
import datetime

TIME_STR_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_SEC_DAY = 24*60*60

def match_str(key):
    # '2019-01-01 00:00:00'
    p = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
    pattern = re.compile(p)
    match = re.match(pattern, key)
    if not match:
        return None
    else:
        return match.span()

TimeType = {
    'err':-1,
    'str':0,
    'int':1,
    'date':2,
    'float':3,
}

class TimeUnit(object):

    def __init__(self, time):
        'time can be str/int/date'
        type = self.time_type(time)
        assert not type==TimeType['err'], 'format error'

        if type==TimeType['str']:
            self.str = time
            self.sec = TimeUnit.str2sec(time)
            self.date = TimeUnit.str2date(time)
        elif type==TimeType['int'] or type==TimeType['float']:
            self.sec = time
            self.str = TimeUnit.sec2str(time)
            self.date = TimeUnit.sec2date(time)
        elif type==TimeType['date']:
            self.date = time
            self.sec = TimeUnit.date2sec(time)
            self.str = TimeUnit.date2str(time)

    @classmethod
    def str2sec(cls, str):
        time_array = time.strptime(str, TIME_STR_FORMAT)
        return int(time.mktime(time_array))

    @classmethod
    def str2date(cls, str):
        return datetime.datetime.strptime(str, TIME_STR_FORMAT)

    @classmethod
    def sec2str(cls, sec):
        time_array = time.localtime(sec)
        return time.strftime(TIME_STR_FORMAT, time_array)

    @classmethod
    def sec2date(cls, sec):
        return datetime.datetime.utcfromtimestamp(sec)

    @classmethod
    def date2str(cls, date):
        return date.strftime(TIME_STR_FORMAT)

    @classmethod
    def date2sec(cls, date):
        return time.mktime(date.timetuple())

    @classmethod
    def s2t(cls, str):
        h,m,s = str.strip().split(":")
        return int(h)*3600 + int(m)*60 + int(s)

    @classmethod
    def t2s(cls, ts):
        m,s = divmod(ts, 60)
        h,m = divmod(m, 60)
        return '{}:{}:{}'.format(h, m, s)

    def time_type(self, time):
        if (not isinstance(time, int)) and\
           (not isinstance(time, float)) and\
           (not isinstance(time, str)) and\
           (not isinstance(time, datetime.datetime)):
           return TimeType['err']

        if (isinstance(time, str) and (not match_str(time))):
            print 'start\'s format must be xx:xx:xx'
            return TimeType['err']

        if (isinstance(time, str)):
            return TimeType['str']
        elif (isinstance(time, int)):
            return TimeType['int']
        elif (isinstance(time, float)):
            return TimeType['float']
        elif (isinstance(time, datetime.datetime)):
            return TimeType['date']

        return TimeType['err']

    def __str__(self):
        return self.str

    def __repr__(self):
        return self.str


class TimeRange(object):

    def __init__(self, start, end):
        self.start = TimeUnit(start)
        self.end = TimeUnit(end)
        assert self.start.sec <= self.end.sec, 'start > end'

    @classmethod
    def str_within(cls, str, range):
        time = TimeUnit(str)
        return TimeRange.sec_within(time.sec, range)

    @classmethod
    def sec_within(cls, sec, range):
        if (sec <= range.end.sec) and (sec >= range.start.sec):
            return True
        else:
            return False

    @classmethod
    def last(cls, window):
        now = time.time()
        before = now - window
        return cls(before, now)

    @classmethod
    def last_day(cls, days_nr=1):
        window = TIME_SEC_DAY*days_nr
        return cls.last(window)

    @classmethod
    def last_month(cls, months_nr=1):
        window = 30*TIME_SEC_DAY*months_nr
        return cls.last(window)

    @classmethod
    def last_year(cls, years_nr=1):
        window = 365*30*TIME_SEC_DAY*years_nr
        return cls.last(window)

    def __str__(self):
        return '{} to {}'.format(self.start, self.end)


def datatime_to_ts(datatime):
    time_array = time.strptime(datatime, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(time_array))

def ts_to_datatime(ts):
    time_array = time.localtime(ts)
    return time.strftime("%Y-%m-%d %H:%M:%S", time_array)

def time_range_get(time_start, time_stop):
    range = {
        "time_start":time_start,
        "time_stop":time_stop,
        "start_ts":0,
        "stop_ts":0
    }

    range["start_ts"] = datatime_to_ts(time_start)
    range["stop_ts"] = datatime_to_ts(time_stop)
    return range

def _time_range_get(window):
    range = {
        "time_start":"",
        "time_stop":"",
        "start_ts":0,
        "stop_ts":0
    }

    now = time.time()
    range["start_ts"] = now - window
    range["stop_ts"] = now
    range["time_start"] = ts_to_datatime(range["start_ts"])
    range["time_stop"] = ts_to_datatime(range["stop_ts"])
    return range

def time_range_get_day(day=1):
    window = 24*60*60*day
    return _time_range_get(window)

def time_range_get_month(month=1):
    window = 30*24*60*60*month
    return _time_range_get(window)

def time_range_get_year(year=1):
    window = 12*30*24*60*60*year
    return _time_range_get(window)

def time_within_range(ts, range):
    if (ts <= range["stop_ts"]) and (ts >=range["start_ts"]):
        return True
    else:
        return False

def time_equl(ts1, ts2):
    if (ts1 == ts2) or (abs(ts1-ts2) < 0.5):
        return True
    else:
        return False
