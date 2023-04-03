# Pico-RGB-Matrix-Clock
LED Matrix Clock with weather running on a Raspberry Pico W and a WaveShare [Pico-RGB-Matrix-P3-64x32](https://www.waveshare.com/wiki/Pico-RGB-Matrix-P3-64x32)

## Weather APIs
A subscription to Open Weather Map (OWM) is required to display the current conditions and the current condition icon. Tempest api is optional, if provided it will pull all information except the above two items from OWM.

### [Open Weather Map](https://openweathermap.org)
Go to the [OWM sign up](https://openweathermap.org/appid) and using the free subscription is enough to create a working Token for this project.
Put the token from the [OWM API Keys page](https://home.openweathermap.org/api_keys) into the settings.toml file in the OWM_API_TOKEN="" setting.
OWM uses your geolocation which gets looked up via the Geolocation api, for this you need to provide your zipcode and the Country under OWM settings listed below.
Be sure to enable the OWM api by setting the OWM_ENABLE=1 to turn it on.

### [Tempest](https://tempestwx.com/)
Sign into your tempest portal to create a application token under [Settings](https://tempestwx.com/settings) and find your stationID (in the URL after you sign up).
Put the token from [Data Authorizations](https://tempestwx.com/settings/tokens) in the settings.toml file under TEMPEST_API_TOKEN="" and enter the station under the TEMPEST_STATION=xxxxx  where xxxxx is the number from tempestwx.com/station/xxxxx/
Be sure to enable the tempest api by setting the TEMPEST_ENABLE=1 to turn it on.

## Settings
Requires a settings.toml file with the following settings in settings file:

* WIFI_SSID="your ssid"
* WIFI_PASSWORD="yoursupersecretpassword"
* NTP_HOST="0.adafruit.pool.ntp.org"
* TZ_OFFSET=<timezone offset> ie TZ_OFFSET=-5
* NTP_INTERVAL=6
* UNITS="imperial" # imperial or metric
### tempestwx.com (tempest) Data Authorization
* TEMPEST_ENABLE=0 # 0 = disabled, 1 = enabled
* TEMPEST_API_TOKEN="yourDataAuthorizationToken"
* TEMPEST_STATION=0 #YourStationNumber
### openweathermap.org Data Authorization
* OWM_ENABLE=0 # 0 = disabled, 1 = enabled
* OWM_API_TOKEN="Your Token"
* OWM_ZIP="zip/post code"
* OWM_COUNTRY="US" # Please use ISO 3166 country codes

## Persistant Settings
To enable in application settings you must rename the _boot.py file to boot.py and place it on your device.  

With this setting enabled any changes to the in menu setting ( Buzzer/ Autodim / 12/24 hr clock / DST Adjust ) will persist when you turn the device off and turn it back on again. 

Settings:
* APPLY DST - Moves time ahead by 1 hour (you must manually turn it on and off) ** Only Works with NTP enabled **
* BEEP SET - Turns the beeping for button presses on and off 
* AUTODIM - When the light sensor detects its dark it will dim the display (turn the LED display off). 
* 12/24 HR - Changes the clock between 12 and 24 hour display.

**NOTE** When boot.py is enabled the drive becomes read only for your computer, to make changes you must hold down the menu / KEY0 button (Bottom button) when you turn on the device. This setting is only read at boot and restarting will have no effect on this setting. 

## Board
This project requires the use of a [Raspberry Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/) to use the WIFI for getting information for displaying on the screen such as updated time, and eventually local weather. (api to be defined soon)

## Circuitpython 8.0.0
This project requires that you use [circuitpython 8.x.x](https://circuitpython.org/board/raspberry_pi_pico_w/). 

## Libraries
Circuit libraries are included in the ./lib/src folder, just copy the ./src folder to the Pico. Most of the libraries are located on the 
 CircuitPython [libraries](https://circuitpython.org/libraries) page. 
 Notes: 
 * The schedule library is located in the version 8.x Community Bundle. 
 * The IR_RX library is located on [github](https://github.com/peterhinch/micropython_ir).

## Clock
Connects to a Network Time Protocol server (0.adafruit.pool.ntp.org) and sets the onboard DS3231 RTC based on the time from the NTP response.

## Weather Plugin
Not implemented yetS

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

# KNOWN ISSUES
* Buttons to go into settings do not work when in autodim mode.
