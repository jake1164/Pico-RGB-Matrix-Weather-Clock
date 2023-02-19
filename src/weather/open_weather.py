## Pulls the weather from the openweathermap.org api. 
import os

# NOTE: https seems to cause an issue but http works fine for this api
GEO_URL = 'http://api.openweathermap.org/geo/1.0/zip?zip={},{}&appid={}'
URL = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units={}&appid={}'


class OpenWeather():
    def __init__(self, network, units) -> None:
        self._units = units
        self._network = network
        token = os.getenv('OWM_API_TOKEN')
        zip = os.getenv('OWM_ZIP')
        country = os.getenv('OWM_COUNTRY')
        # TODO: check parameters here and ensure geo works.
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
        #print(weather)
        # TODO: reduce size of json data and purge gc
        return weather


    ''' Show just the current condtions and maps '''
    def show_secondary(self, display, weather=None):
        if not weather:
            weather = self.get_weather()
        display.set_icon(weather["weather"][0]["icon"])
        display.set_description(weather["weather"][0]["description"])
        


    ''' Show the weather and conditions from OWM '''
    def show_weather(self, display):
        print('updating weather')
        weather = self.get_weather()

        display.set_temperature(weather["main"]["temp"])        
        display.set_humidity(weather["main"]["humidity"])
        display.set_feels_like(weather["main"]["feels_like"])
        display.set_wind(weather["wind"]["speed"])
        self.show_secondary(display, weather)
        display.show()
