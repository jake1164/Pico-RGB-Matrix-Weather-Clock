# Pico-RGB-Matrix-Clock
LED Matrix Clock with weather running on a Raspberry Pico W and a WaveShare Pico-RGB-Matrix-P3-64x32

Currently based on sample code with modifications added to support a pico W. 

## Settings
Requires a settings.toml file with the following settings in settings file:
* TZ_OFFSET=<timezone offset> ie TZ_OFFSET=-5
* WIFI_SSID="your ssid"
* WIFI_PASSWORD="yoursupersecretpassword"
* NTP_HOST="0.adafruit.pool.ntp.org"
* NTP_INTERVAL=6  

## Clock
Connects to a Network Time Protocol server (0.adafruit.pool.ntp.org) and sets the onboard DS3231 RTC based on the time from the NTP response.

## Weather Plugin

