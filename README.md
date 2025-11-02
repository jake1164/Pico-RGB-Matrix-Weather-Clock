# Pico-RGB-Matrix-Weather-Clock
LED Matrix Clock with Open Weather Map enabled weather running on a Raspberry Pico W and a WaveShare [Pico-RGB-Matrix-P3-64x32](https://www.waveshare.com/wiki/Pico-RGB-Matrix-P3-64x32)

## NOTE: Works with CircuitPython 9.x or 10.x
This project requires that you use [CircuitPython 9.x or 10.x](https://circuitpython.org/board/raspberry_pi_pico_w/). 
If you still wish to use 8.x you will need to use an older [release](https://github.com/jake1164/Pico-RGB-Matrix-Weather-Clock/releases/tag/v0.54.0)

## Weather APIs
An account on Open Weather Map (OWM) is required to display the current conditions and the current condition icon. 

### [Open Weather Map](https://openweathermap.org)
Go to the [OWM sign up](https://openweathermap.org/appid) and using the free subscription is enough to create a working Token for this project.
Put the token from the [OWM API Keys page](https://home.openweathermap.org/api_keys) into the settings.toml file in the OWM_API_TOKEN="" setting.
Uses the OpenWeather Geocoding API to resolve your ZIP + Country to latitude/longitude, so provide ZIP and Country under OWM settings below.

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
* WEATHER_TIMEOUT=300 **Watchdog seconds before forced reset if no weather during active period**

### openweathermap.org Data Authorization
* OWM_ENABLE_WEATHER=1 # 0 disables weather, removing or setting to 1 enables weather
* OWM_API_TOKEN="Your Token"
* OWM_ZIP="zip/post code"
* OWM_COUNTRY="US" # Please use ISO 3166 country codes
* OWM_USE_HTTPS=0 # Set to 1 to request via https:// instead of http://

## Persistent Settings
To enable you must rename the _boot.py file to boot.py on your device.  

With this setting enabled any changes to the in menu setting ( Buzzer/ Autodim / 12/24 hr clock / Net Time / DST Adjust ) will persist when you turn the device off and turn it back on again. 

Settings:
* NET TIME - Enables automatic time synchronization from Network Time Protocol (NTP) server. When enabled, time is automatically fetched from the internet based on your timezone offset. **Note: NET TIME does not automatically handle Daylight Saving Time - you must manually toggle APPLY DST.**
* APPLY DST - Adds 1 hour for Daylight Saving Time. When NET TIME is enabled, this adjusts the NTP time by +1 hour. When NET TIME is disabled, this manually adjusts the clock by +1 hour. You must manually turn this on/off when entering or leaving DST.
* BEEP SET - Turns the beeping for button presses on and off 
* AUTODIM - When the light sensor detects darkness it will dim the display (turn the LED display off). 
* 12/24 HR - Changes the clock between 12 and 24 hour display.

**NOTE** When boot.py is enabled the drive becomes read only for your computer, to make changes you must hold down the menu / KEY0 button (Bottom button) when you turn on the device. This setting is only read at boot and restarting will have no effect on this setting. 

## Board
This project works with a [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/) or the newer [Raspberry Pi Pico W 2]. It uses Wi‑Fi for time and local weather updates.

## CircuitPython 9.x or 10.x
This project requires that you use [CircuitPython 9.x or 10.x](https://circuitpython.org/board/raspberry_pi_pico_w/). 

## Quick Start
1. Install CircuitPython 9.x or 10.x on your Pico W or Pico W 2.
2. Copy the contents of `src/` to the CIRCUITPY drive root (do not copy the folder itself).
3. Rename `src/settings.toml.default` to `settings.toml` and edit:
   - `WIFI_SSID`, `WIFI_PASSWORD`, `NTP_HOST`, `TZ_OFFSET`, `NTP_INTERVAL`
   - `OWM_API_TOKEN`, `OWM_ZIP`, `OWM_COUNTRY`, `UNITS` (and optionally `OWM_USE_HTTPS=1`)
   - Optionally adjust `WEATHER_TIMEOUT`
4. Optional: for persistent menu settings, rename `src/_boot.py` to `boot.py` on the device. Note: this makes the drive read-only; to write again, hold the Menu/KEY0 button at power‑on.
5. Safely eject and power cycle the Pico W.

## Hardware
- Required: Raspberry Pi Pico W or Pico W 2; WaveShare Pico‑RGB‑Matrix‑P3‑64x32 panel.
- RTC: External DS3231 on I2C (SCL `GP7`, SDA `GP6`).
- Buttons: Uses `GP15`, `GP19`, `GP21` (on the Waveshare base board).
- Optional: Light sensor on `GP26` for auto-dim; Buzzer on `GP27`.

## Libraries
CircuitPython libraries are included in `./src/lib`. Copy the contents of `./src` to the CIRCUITPY drive root (do not copy the folder itself). Most of the libraries are located on the CircuitPython [libraries](https://circuitpython.org/libraries) page.

## Clock
Connects to a Network Time Protocol server (e.g., `0.adafruit.pool.ntp.org`) and sets an external DS3231 RTC module (I2C SCL `GP7`, SDA `GP6`) based on the NTP time.

## Images
![figure 1](/images/img1.jpg)
![figure 2](/images/img2.jpg)
![figure 3](/images/img3.jpg)
![figure 4](/images/img4.jpg)

# Code Standards
This project moving forward will be converting changed code to loosely meet the
google python [coding standard](https://google.github.io/styleguide/pyguide.html#316-naming). 

## VS Code Settings
To ignore the `code.py` overriding standard library warning, add the following
to your `.vscode/settings.json` config file.
```
  "python.languageServer": "Pylance",
  [...]
  "python.analysis.diagnosticSeverityOverrides": {
      "reportShadowedImports": "none"
  },
```
