import time
import busio
import board
import adafruit_ds3231


class DateTimeProcessing:


    def __init__(self, format, network) -> None:
        self.DAYS_OF_WEEK = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday" )
        self._MAX_DAYS = [None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self._DAYS_BEFORE_MONTH = (None, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)
        self.network = network
        self.time_format = format
        self.time = [0, 0, 0]
        self.date = [0, 0, 0]
        i2c = busio.I2C(board.GP7,board.GP6)  # uses board.SCL and board.SDA
        self.rtc = adafruit_ds3231.DS3231(i2c)


    def update_from_ntp(self):
        try:
            new_time = self.network.get_time()
            print(new_time)
            self.rtc.datetime = new_time
            print('updated RTC datetime')
        except Exception as e:
            print('update exception', e)


    def get_interval(self):
        return self.network.get_interval()


    def is_12hr(self):
        if self.time_format == 0: # 12 hour            
            return True
        else:
            return False


    def toggle_time_format(self):
        if self.is_12hr():
            self.time_format = 1
        else:
            self.time_format = 0


    def get_date(self):
        dt = self.rtc.datetime
        return "%04d" % dt.tm_year + '-' + "%02d" % dt.tm_mon + '-' + "%02d" % dt.tm_mday


    def get_time(self):
        dt = self.rtc.datetime
        time = ''
   
        if self.is_12hr(): # 12 hour
            if dt.tm_hour == 0:
                hour = 12
            elif dt.tm_hour < 13:
                hour = dt.tm_hour
            else:
                hour = dt.tm_hour - 12
                
            time = "{:2d}:{:02d}{}".format(
                hour,
                dt.tm_min,
                "pm" if dt.tm_hour > 11 else "am")
        else: # 24 hour
            time = "%02d" % dt.tm_hour + ':' + "%02d" % dt.tm_min + ':' + "%02d" % dt.tm_sec

        return time


    def get_setting_time(self, update):
        # update the time array to current time
        if update:
            dt = self.rtc.datetime
            self.time[0] = dt.tm_hour
            self.time[1] = dt.tm_min
            self.time[2] = dt.tm_sec
        # format and return the string.
        return "%02d" % self.time[0] + ':' + "%02d" % self.time[1] + ':' + "%02d" % self.time[2]


    def get_setting_date(self, update):
        if update:
            dt = self.rtc.datetime
            self.date[0] = dt.tm_year
            self.date[1] = dt.tm_mon
            self.date[2] = dt.tm_mday
        return "%02d" % self.date[0] + '-' + "%02d" % self.date[1] + '-' + "%02d" % self.date[2]


    def get_dow(self):
        time = self.rtc.datetime
        return self.DAYS_OF_WEEK[int(time.tm_wday)]


    def set_hour(self, increment):
        if increment:
            self.time[0] += 1
            if self.time[0] == 24:
                self.time[0] = 0
        else:
            self.time[0] -= 1
            if self.time[0] < 0:
                self.time[0] = 23



    def set_min(self, increment):
        if increment:
            self.time[1] += 1
            if self.time[1] == 60:
                self.time[1] = 0
        else:
            self.time[1] -= 1
            if self.time[1] < 0:
                self.time[1] = 59


    def set_sec(self, increment):
        if increment:
            self.time[2] += 1
            if self.time[2] == 60:
                self.time[2] = 0
        else:
            self.time[2] -= 1
            if self.time[2] < 0:
                self.time[2] = 59

    def set_day(self, increment):
        if increment:
            self.date[2] += 1
            if self.date[2] > self.get_max_day(self.date[1], self.date[0]):
                self.date[2] = 1
        else:
            self.date[2] -= 1
            if self.date[2] < 1:
                self.date[2] = self.get_max_day(self.date[1], self.date[0])

    def set_month(self, increment):
        if increment:
            self.date[1] += 1
            if self.date[1] > 12:
                self.date[1] = 1
        else:
            self.date[1] -= 1
            if self.date[1] < 1:
                self.date[1] = 12

    def set_year(self, increment):
        if increment:
            self.date[0] += 1
            if self.date[0] > 2099:
                self.date[0] = 2000
        else:
            self.date[0] -= 1
            if self.date[0] < 2000:
                self.date[0] = 2099


    def is_leap_year(self, year):
        "year -> 1 if leap year, else 0."
        if year % 4 == 0 and year % 100 != 0:
            return True
        if year % 400 == 0:
            return True
        return False


    def get_max_day(self, month, year):
        if month < 1 or month > 12:
            print("error month")
            return -1
        maxDay = self._MAX_DAYS[month]
        if year != -1 and month == 2:
            if self.is_leap_year(year):
                maxDay += 1
        return maxDay


    def set_datetime(self, option):
        getTime = self.rtc.datetime
        if option == 0:
            t = time.struct_time((getTime.tm_year, getTime.tm_mon, getTime.tm_mday, self.time[0], self.time[1], self.time[2], getTime.tm_wday, -1, -1))
            self.rtc.datetime = t
        if option == 1:
            w = (self.ymd2ord(self.date[0],self.date[1], self.date[2]) + 6) % 7            
            t = time.struct_time((self.date[0], self.date[1], self.date[2], getTime.tm_hour, getTime.tm_min, getTime.tm_sec, w, -1, -1))
            self.rtc.datetime = t


    def ymd2ord(self, year, month, day):
        "year, month, day -> ordinal, considering 01-Jan-0001 as day 1."
        assert 1 <= month <= 12, "month must be in 1..12"
        dim = self._days_in_month(year, month)
        assert 1 <= day <= dim, "day must be in 1..%d" % dim
        return self._days_before_year(year) + self._days_before_month(year, month) + day


    def _days_in_month(self, year, month):
        "year, month -> number of days in that month in that year."
        assert 1 <= month <= 12, month
        if month == 2 and self.is_leap_year(year):
            return 29
        return self._MAX_DAYS[month]


    def _days_before_month(self, year, month):
        "year, month -> number of days in year preceding first day of month."
        assert 1 <= month <= 12, "month must be in 1..12"
        return self._DAYS_BEFORE_MONTH[month] + (month > 2 and self.is_leap_year(year))


    def _days_before_year(self, year):
        "year -> number of days before January 1st of year."
        year = year - 1
        return year * 365 + year // 4 - year // 100 + year // 400