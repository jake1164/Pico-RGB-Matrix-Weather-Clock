# Pulls weather from a the weatherflow api (from a tempest weather station) 
# https://weatherflow.github.io/Tempest/api/ 
import os
import displayio
from terminalio import FONT
from adafruit_display_text.label import Label
from . import base_weather

STATIONS_URL = 'https://swd.weatherflow.com/swd/rest/stations?token={}'
URL = 'http://swd.weatherflow.com/swd/rest/observations/station/{}?token={}'
BETTER_URL = 'https://swd.weatherflow.com/swd/rest/better_forecast?station_id={}&units_temp=f&units_wind=mph&units_pressure=mmhg&units_precip=in&units_distance=mi&token={}'

class TempestWeather(base_weather.BaseDisplay):
    def __init__(self, display, network) -> None:
        super().__init__()
        self._display = display
        self._network = network
        token = os.getenv('TEMPEST_API_TOKEN')
        station = os.getenv('TEMPEST_STATION')
        self._url = URL.format(station, token)

        #self.root_group = displayio.Group()
        #self.root_group.append(self)
        #self._text_group = displayio.Group()
        #self._icon_group = displayio.Group()
        #self._scrolling_group = displayio.Group()

        ##self.append(self._text_group) 
        #self.temperature = Label(FONT, color=0x00DD00)
        #self.temperature.x = 20
        #self.temperature.y = 7
        #self._text_group.append(self.temperature)
        #self.append(self._scrolling_group)
        #self.append(self._icon_group)



    def get_weather(self):
        weather = self._network.getJson(self._url)
        #print(weather)
        # TODO: reduce size of json data and purge gc

        return weather


    def get_update_interval(self):
        """ Returns the weather update interval in seconds """
        return 20

    def show_weather(self):
        weather = self.get_weather()
        print(weather)
        self.temperature.text = self._convert_to_fahrenheit(weather["obs"][0]["air_temperature"])
        print('updating weather')
        self._display.show(self.root_group)


    def _convert_to_fahrenheit(self, celsius) -> str:
        return str((celsius * 1.8) + 32)