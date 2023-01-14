# Pico-RGB-Matrix-Clock
LED Matrix Clock with weather running on a Raspberry Pico W and a WaveShare [Pico-RGB-Matrix-P3-64x32](https://www.waveshare.com/wiki/Pico-RGB-Matrix-P3-64x32)

Currently a fork of the waveshare sample code with modifications added to support a pico W and 12 / 24 hour display option.

## Board
This project requires the use of a [Raspberry Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/) to use the WIFI for getting information for displaying on the screen such as updated time, and eventually local weather. (api to be defined soon)

## Circuitpython 8.0.0
This project requires that you use [circuitpython 8.0.0](https://circuitpython.org/board/raspberry_pi_pico_w/) which is currently in beta. 

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
Not implemented yetS

