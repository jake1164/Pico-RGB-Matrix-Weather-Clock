# Pulls weather from a the weatherflow api (from a tempest weather station) 
# https://weatherflow.github.io/Tempest/api/ 
import os
import displayio
from terminalio import FONT
from adafruit_display_text.label import Label

STATIONS_URL = 'https://swd.weatherflow.com/swd/rest/stations?token={}'
URL = 'http://swd.weatherflow.com/swd/rest/observations/station/{}?token={}'
#BETTER_URL = 'https://swd.weatherflow.com/swd/rest/better_forecast?station_id={}&units_temp=f&units_wind=mph&units_pressure=mmhg&units_precip=in&units_distance=mi&token={}'

class TempestWeather():
    def __init__(self, network, units) -> None:
        self._units = units
        self._network = network
        token = os.getenv('TEMPEST_API_TOKEN')
        station = os.getenv('TEMPEST_STATION')
        self._url = URL.format(station, token)
        #self._url = BETTER_URL.format(station, token)

    def get_weather(self):
        weather = self._network.getJson(self._url)
        #print(weather)
        # TODO: reduce size of json data and purge gc

        return weather


    def get_update_interval(self):
        """ Returns the weather update interval in seconds """
        return 20

    def show_weather(self, weather_display):
        weather = self.get_weather()
        print(weather)
        if weather == {}:
            return
        weather_display.set_temperature(self._convert_to_fahrenheit(weather["obs"][0]["air_temperature"]))
        weather_display.show()


    def _convert_to_fahrenheit(self, celsius):
        return (celsius * 1.8) + 32