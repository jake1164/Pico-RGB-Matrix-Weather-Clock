_MAX_DAYS = [None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
_DAYS_BEFORE_MONTH = (None, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)
DAYS_OF_WEEK = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday" )

def is_leap_year(year):
    "year -> 1 if leap year, else 0."
    if year % 4 == 0 and year % 100 != 0:
        return True
    if year % 400 == 0:
        return True
    return False


def get_max_day(month, year):
    if month < 1 or month > 12:
        print("error month")
        return -1
    maxDay = _MAX_DAYS[month]
    if year != -1 and month == 2:
        if is_leap_year(year):
            maxDay += 1
    return maxDay


def ymd2ord(year, month, day):
    "year, month, day -> ordinal, considering 01-Jan-0001 as day 1."
    assert 1 <= month <= 12, "month must be in 1..12"
    dim = _days_in_month(year, month)
    assert 1 <= day <= dim, "day must be in 1..%d" % dim
    return _days_before_year(year) + _days_before_month(year, month) + day


def _days_in_month(year, month):
    "year, month -> number of days in that month in that year."
    assert 1 <= month <= 12, month
    if month == 2 and is_leap_year(year):
        return 29
    return _MAX_DAYS[month]


def _days_before_month(year, month):
    "year, month -> number of days in year preceding first day of month."
    assert 1 <= month <= 12, "month must be in 1..12"
    return _DAYS_BEFORE_MONTH[month] + (month > 2 and is_leap_year(year))


def _days_before_year(year):
    "year -> number of days before January 1st of year."
    year = year - 1
    return year * 365 + year // 4 - year // 100 + year // 400