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
    def __init__(self, display, network, datetime) -> None:
        super().__init__(display)
        #self._display = display
        self._network = network
        self._datetime = datetime
        token = os.getenv('OWM_API_TOKEN')
        zip = os.getenv('OWM_ZIP')
        country = os.getenv('OWM_COUNTRY')    
        lat, lon = self._get_geo(zip, country, token)        
        self._url = URL.format(lat, lon, self._units, token)      


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
        self.set_time(self._datetime.get_time())
        self.set_temperature(weather["main"]["temp"])        
        self.set_icon(weather["weather"][0]["icon"])
        self.set_humidity(weather["main"]["humidity"])
        self.set_description(weather["weather"][0]["description"])
        self.set_feels_like(weather["main"]["feels_like"])
        self.set_date(
            self._datetime.get_date()    
        )
        
        print('updating weather')
        self._display.show(self.root_group)
        