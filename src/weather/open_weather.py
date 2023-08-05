## Pulls the weather from the openweathermap.org api. 
import os

# NOTE: https seems to cause an issue but http works fine for this api
GEO_URL = 'http{}://api.openweathermap.org/geo/1.0/zip?zip={},{}&appid={}'
URL = 'http{}://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units={}&appid={}'


class OpenWeather():
    def __init__(self, weather_display, datetime, network) -> None:
        self._display_current = None
        self._weather_display = weather_display
        self._network = network
        self._datetime = datetime
        token = os.getenv('OWM_API_TOKEN')
        zip = os.getenv('OWM_ZIP')
        country = os.getenv('OWM_COUNTRY')
        https = 's' if os.getenv('OWM_USE_HTTPS') == 1 else ''
        # TODO: check parameters here and ensure geo works.
        lat, lon = self._get_geo(https, zip, country, token)        
        self._url = URL.format(https, lat, lon, weather_display.units, token)      


    def _get_geo(self, https, zip, country, token):
        # TODO: Need some better error handling here
        geo_url = GEO_URL.format(https, zip, country, token)
        geo = self._network.getJson(geo_url)
        if geo == None or geo == {}:
            raise Exception('Unable to get geo')
        
        return geo['lat'], geo['lon']


    def get_update_interval(self):
        """ Returns the weather update interval in seconds """
        return 20


    def get_weather(self):
        weather = self._network.getJson(self._url)
        #print(weather)
        # TODO: reduce size of json data and purge gc
        return weather

    def show_datetime(self) -> bool:
        self._weather_display.set_time(self._datetime.get_time())

        # Only adjust the brightness once
        if self._datetime.display_on != self._display_current:
            self._weather_display.brightness = 0.1 if self._datetime.display_on else 0.0
            self._display_current = self._datetime.display_on

        if self._datetime.display_on:            
            self._weather_display.show()            

        return self._display_current
         

    ''' Show the weather and conditions from OWM '''
    def show_weather(self):
        try:
            weather = self.get_weather()
        except Exception as ex:
            print('Unable to get weather', ex)
            weather = None

        # Always add the date so there is something to scroll.
        self._weather_display.set_date(
            self._datetime.get_date()
        )

        if weather == None or weather == {} or weather["main"] == None:
            return
        try:            
            self._weather_display.set_temperature(weather["main"]["temp"])        
            self._weather_display.set_icon(weather["weather"][0]["icon"])
            # add Scrolling items
            # TODO: These should really be a list of items that can be added and tracked easier.
            self._weather_display.set_humidity(weather["main"]["humidity"])
            self._weather_display.set_feels_like(weather["main"]["feels_like"])
            self._weather_display.set_wind(weather["wind"]["speed"])            
            self._weather_display.set_description(weather["weather"][0]["description"])
        except Exception as e:
            print('Unable to display weather', e)
        finally:
            self._weather_display.show()

    def weather_complete(self) -> bool:        
        return not self._weather_display.scroll_queue