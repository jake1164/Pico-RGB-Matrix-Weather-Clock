# Pico-RGB-Matrix-Clock
LED Matrix Clock with Open Weather Map enabled weather running on a Raspberry Pico W and a WaveShare [Pico-RGB-Matrix-P3-64x32](https://www.waveshare.com/wiki/Pico-RGB-Matrix-P3-64x32)

## Weather APIs
An account on Open Weather Map (OWM) is required to display the current conditions and the current condition icon. 

### [Open Weather Map](https://openweathermap.org)
Go to the [OWM sign up](https://openweathermap.org/appid) and using the free subscription is enough to create a working Token for this project.
Put the token from the [OWM API Keys page](https://home.openweathermap.org/api_keys) into the settings.toml file in the OWM_API_TOKEN="" setting.
OWM uses your geolocation which gets looked up via the Geolocation API, for this you need to provide your zip code and the Country under OWM settings listed below.

### NTP Servers 
You can define up to 3 NTP servers, one primary and two fallbacks, to use for time synchronization. The servers are separated by a "pipe" | character. You can find a list of [NTP Servers](https://timetoolsltd.com/information/public-ntp-server/) to use if you need something closer. 

## Settings
Requires a settings.toml file with the following settings in settings file.
A settings.toml.default file has been provided with the required settings for the application. Copy or rename the settings.toml.default file to settings.toml.

* WIFI_SSID="your ssid"
* WIFI_PASSWORD="yoursupersecretpassword"
* NTP_HOST="0.adafruit.pool.ntp.org|0.us.pool.ntp.org"
* TZ_OFFSET=-5 
* NTP_INTERVAL=21600 **ie 21600 = 6hr, 43200 = 12hr, 86400 = 24hr**
* UNITS="imperial" **ie imperial or metric**

### openweathermap.org Data Authorization
* OWM_ENABLE_WEATHER=1 # 0 disables weather, removing or setting to 1 enables weather
* OWM_API_TOKEN="Your Token"
* OWM_ZIP="zip/post code"
* OWM_COUNTRY="US" # Please use ISO 3166 country codes

## Persistent Settings
To enable you must rename the _boot.py file to boot.py on your device.  

With this setting enabled any changes to the in menu setting ( Buzzer/ Autodim / 12/24 hr clock / DST Adjust ) will persist when you turn the device off and turn it back on again. 

Settings:
* APPLY DST - Moves time ahead by 1 hour (you must manually turn it on and off) ** Only Works with NTP enabled **
* BEEP SET - Turns the beeping for button presses on and off 
* AUTODIM - When the light sensor detects darkness it will dim the display (turn the LED display off). 
* 12/24 HR - Changes the clock between 12 and 24 hour display.

**NOTE** When boot.py is enabled the drive becomes read only for your computer, to make changes you must hold down the menu / KEY0 button (Bottom button) when you turn on the device. This setting is only read at boot and restarting will have no effect on this setting. 

## Board
This project requires the use of a [Raspberry Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/) to use the WIFI for getting information for displaying on the screen such as updated time, and local weather.

## CircuitPython 8.0.0
This project requires that you use [circuitpython 8.x.x](https://circuitpython.org/board/raspberry_pi_pico_w/). 

## Libraries
Circuit libraries are included in the ./lib/src folder, just copy the ./src folder to the Pico. Most of the libraries are located on the 
 CircuitPython [libraries](https://circuitpython.org/libraries) page. 
 Notes: 
* The IR_RX library is located on [github](https://github.com/peterhinch/micropython_ir).

## Clock
Connects to a Network Time Protocol server (0.adafruit.pool.ntp.org) and sets the onboard DS3231 RTC based on the time from the NTP response.

## Images
![figure 1](/images/img1.jpg)
![figure 2](/images/img2.jpg)
![figure 3](/images/img3.jpg)
![figure 4](/images/img4.jpg)

# Code Standards
This project moving forward will be converting changed code to loosely meet the
google python [coding standard](https://google.github.io/styleguide/pyguide.html#316-naming). 

## pylint settings
To ignore the code.py overriding the std lib error add the following
to your .vscode.json config file.
```
  "python.languageServer": "Pylance",
  [...]
  "python.analysis.diagnosticSeverityOverrides": {
      "reportShadowedImports": "none"
  },
```
