MAX_DAYS = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# used in getMaxDay
def is_leap_year(year):
    if year % 4 == 0 and year % 100 != 0:
        return True
    if year % 400 == 0:
        return True
    return False

# Used in keydown & keyup processing to set date
def get_max_day(month, year):
    if month < 1 or month > 12:
        print("error month")
        return -1
    maxDay = MAX_DAYS[month]
    if year != -1 and month == 2:
        if is_leap_year(year):
            maxDay += 1
    return maxDay
