## Pulls the weather from the openweathermap.org api. 
## Should this implement the weather display as well?  

import os
GEO_URL = 'http://api.openweathermap.org/geo/1.0/zip?zip={},{}&appid={}'
# NOTE: https seems to cause an issue but http works fine for this api
URL = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=imperial&appid={}'

class OpenWeather():
    def __init__(self, network) -> None:
        self.network = network
        token = os.getenv('OWM_API_TOKEN')
        # I dont think I need these after init
        zip = os.getenv('OWM_ZIP')
        country = os.getenv('OWM_COUNTRY')
        lat, lon = self._get_geo(zip, country, token)        
        self._url = URL.format(lat, lon, token)

    
    def _get_geo(self, zip, country, token):
        # TODO: Need some better error handling here
        geo_url = GEO_URL.format(zip, country, token)
        geo = self.network.getJson(geo_url)
        return geo['lat'], geo['lon']


    def get_weather(self):
        weather = self.network.getJson(self._url)
        print(weather)

    def get_update_interval(self):
        """ Returns the weather update interval in seconds """
        return 20


