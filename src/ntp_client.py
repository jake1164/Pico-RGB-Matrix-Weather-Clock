# Requires a settings.toml file with the following
# settings in settings file:
# TZ_OFFSET=<timezone offset> ie TZ_OFFSET=-5
# WIFI_SSID="your ssid"
# WIFI_PASSWORD="yoursupersecretpassword"
# NTP_HOST="0.adafruit.pool.ntp.org"
# NTP_INTERVAL=6  

import os
import ipaddress
import wifi
import socketpool
import adafruit_ntp
import busio
import board
import adafruit_ds3231
import time

RETRY = 5 # Number of times to attempt to connect to wifi
TZ = os.getenv('TZ_OFFSET')
NTP_HOST = os.getenv('NTP_HOST')
SSID = os.getenv('WIFI_SSID')
PASS = os.getenv('WIFI_PASSWORD')
INTERVAL = os.getenv('NTP_INTERVAL')

def get_time():       
    # Need better connection testing
    attempt = 1
    while(attempt <= RETRY):
        print('attempting to get time: try ', attempt)
        try:
            if wifi.radio.ipv4_address is not None:
                pool = socketpool.SocketPool(wifi.radio)
                ntp = adafruit_ntp.NTP(pool, tz_offset=TZ, server=NTP_HOST)
                return ntp.datetime
            else:
                wifi.radio.connect(SSID, PASS)
                pool = socketpool.SocketPool(wifi.radio)
                ntp = adafruit_ntp.NTP(pool, tz_offset=TZ, server=NTP_HOST)
                return ntp.datetime
        except Exception as e:
            print(e)
            
        attempt += 1
    raise Exception('Unable to connect')
            

def set_time(time):
    i2c = busio.I2C(board.GP7, board.GP6)
    rtc = adafruit_ds3231.DS3231(i2c)
    rtc.datetime = time
    i2c.deinit()

def update():
    try:
        new_time = get_time()
        set_time(new_time)
    except Exception as ex:
        print('unable to connect', ex)
    
def get_interval():
    return int(INTERVAL)

if __name__ == "__main__":
    new_time = get_time()
    print(new_time)
    set_time(new_time)
    print('updated time')

    time.sleep(2)
    print('Updating again')
    # Testing a second attempt
    new_time = get_time()
    set_time(new_time)
    print('updated time again')
    
