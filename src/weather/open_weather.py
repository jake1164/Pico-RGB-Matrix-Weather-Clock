## Pulls the weather from the openweathermap.org api. 
## Should this implement the weather display as well?  

import os
import displayio
from terminalio import FONT
from adafruit_display_text.label import Label
from . import base_weather

# NOTE: https seems to cause an issue but http works fine for this api
GEO_URL = 'http://api.openweathermap.org/geo/1.0/zip?zip={},{}&appid={}'
URL = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units={}&appid={}'


class OpenWeather(base_weather.BaseDisplay):
    def __init__(self, display, network) -> None:
        super().__init__()
        self._display = display
        self._network = network
        token = os.getenv('OWM_API_TOKEN')
        zip = os.getenv('OWM_ZIP')
        country = os.getenv('OWM_COUNTRY')
        units = os.getenv('UNITS')

        lat, lon = self._get_geo(zip, country, token)        
        self._url = URL.format(lat, lon, units, token)
        
        #self.root_group = displayio.Group()
        #self.root_group.append(self)
        #self._text_group = displayio.Group()
        #self._icon_group = displayio.Group()
        #self._scrolling_group = displayio.Group()
        
        #self.append(self._text_group) 
        #self.temperature = Label(FONT, color=0x00DD00)
        #self.temperature.x = 20
        #self.temperature.y = 7
        #self._text_group.append(self.temperature)
        #self.append(self._scrolling_group)
        #self.append(self._icon_group)
        


    def _get_geo(self, zip, country, token):
        # TODO: Need some better error handling here
        geo_url = GEO_URL.format(zip, country, token)
        geo = self._network.getJson(geo_url)
        return geo['lat'], geo['lon']



    def get_update_interval(self):
        """ Returns the weather update interval in seconds """
        return 20


    def get_weather(self):
        weather = self._network.getJson(self._url)
        print(weather)
        # TODO: reduce size of json data and purge gc

        return weather


    def show_weather(self):
        weather = self.get_weather()
        self.temperature.text = str(weather["main"]["temp"])
        print('updating weather')
        self._display.show(self.root_group)
        