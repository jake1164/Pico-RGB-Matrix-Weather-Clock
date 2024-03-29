## Pulls the weather from the openweathermap.org api. 
import os

# NOTE: https seems to cause an issue but http works fine for this api
GEO_URL = 'http{}://api.openweathermap.org/geo/1.0/zip?zip={},{}&appid={}'
URL = 'http{}://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units={}&appid={}'


class OpenWeather():
    def __init__(self, weather_display, datetime, network) -> None:
        self._weather_display = weather_display
        self._network = network
        self._datetime = datetime
        self._missed_weather = 0
        self.pixel_x = 0
        self.pixel_y = 0
        self._enabled = False if os.getenv('OWM_ENABLE_WEATHER') == 0 else True

        if self._enabled:
            # TODO: check parameters here and ensure geo works.
            token = os.getenv('OWM_API_TOKEN')
            zip = os.getenv('OWM_ZIP')
            country = os.getenv('OWM_COUNTRY')
            https = 's' if os.getenv('OWM_USE_HTTPS') == 1 else ''
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
        if self._enabled:
            weather = self._network.getJson(self._url)
        else:
            weather = {}
        #print(weather)
        # TODO: reduce size of json data and purge gc
        return weather


    def show_datetime(self) -> bool:
        changed = self._weather_display.set_time(self._datetime.get_time())

        if changed and self._datetime.is_display_on:
            self._weather_display.show()

        # display by hour, min        
        
        if self._datetime.is_display_on:
            self._weather_display.hide_pixel(self.pixel_x, self.pixel_y)
        else:
            # Get current pixel being shown
            x = self.pixel_x
            y = self.pixel_y

            # find the new pixel that should be shown
            self.pixel_x = self._datetime.get_minute()
            self.pixel_y = self._datetime.get_hour()

            # If the pixel has changed then hide the old one and show the new one.
            if x != self.pixel_x or y != self.pixel_y:
                # turn off original pixel
                self._weather_display.hide_pixel(x, y)
                #display another pixel.
                self._weather_display.show_pixel(self.pixel_x, self.pixel_y)
        return self._datetime.is_display_on


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
            if not self._enabled:
                return
            elif self._missed_weather > 5:
                self._weather_display.hide_temperature()
                self._weather_display.add_text_display("Unable to contact API")
            else:
                self._missed_weather += 1
            return

        try:
            self._missed_weather = 0
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
    
    def display_off(self):
        self._datetime.is_display_on = False
