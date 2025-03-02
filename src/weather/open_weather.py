## Pulls the weather from the openweathermap.org api. 
import os

# NOTE: https seems to cause an issue but http works fine for this api
GEO_URL = 'http{}://api.openweathermap.org/geo/1.0/zip?zip={},{}&appid={}'
URL = 'http{}://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units={}&appid={}'


class OpenWeather():
    def __init__(self, weather_display, network, datetime) -> None:
        self._weather_display = weather_display
        self._network = network
        self._datetime = datetime

        self._missed_weather = 0
        self.pixel_x = 0
        self.pixel_y = 0
        self._enabled = False if os.getenv('OWM_ENABLE_WEATHER') == 0 else True

        if self._enabled:
            self._url = self._setup_url()


    def _setup_url(self) -> str:
        token = os.getenv('OWM_API_TOKEN')
        zip = os.getenv('OWM_ZIP')
        country = os.getenv('OWM_COUNTRY')
        if token is None or zip is None or country is None:
            raise Exception('Missing required Open Weather Map environment variables for OWM API')
        
        default_units = os.getenv('UNITS')
        if default_units is not None and default_units not in ['imperial', 'metric']:
            raise Exception('Missing required UNITS environment variables')

        https = 's' if os.getenv('OWM_USE_HTTPS') == 1 else ''

        geo_url = GEO_URL.format(https, zip, country, token)
        geo = self._network.getJson(geo_url)
        if geo == None or geo == {}:
            raise Exception('Unable to get geo location from OWM GEO API')
        return URL.format(https, geo['lat'], geo['lon'], default_units, token)


    def _get_units(self) -> str:
        pass


    def get_update_interval(self) -> int:
        """ Returns the weather update interval in seconds """
        return 20


    def get_weather(self) -> dict:
        if self._enabled:
            weather = self._network.getJson(self._url)
        else:
            weather = {}
        #print(weather)
        # TODO: reduce size of json data and purge gc
        return weather


    def _apply_reading(self, field: tuple, weather, func) -> None:
        if isinstance(field[0], int) and isinstance(weather, list) and field[0] < len(weather):
            self._apply_reading(field[1:], weather[field[0]], func)
        elif field and field[0] in weather:
            try:
                # Recursively try each field in the tuple
                if len(field) > 1:
                    self._apply_reading(field[1:], weather[field[0]], func)
                else:
                    # switch to apply the units based on field here. 
                    if field[0] == 'temp': # do temperatue conversion here
                        func(str(weather[field[0]]) + '°')
                    else:
                        func(str(weather[field[0]]))
            except Exception as ex:
                print('Unable to apply reading', ex)
        else:
            print(f'Field {field} not found in weather data')


    def show_weather(self):
        try:
            weather = self.get_weather()
        except Exception as ex:
            print('Unable to get weather', ex)
            weather = None

        # TODO: is this missing from tempest or extranious here?
        # Always add the date so there is something to scroll. 
        self._weather_display.set_date(
            self._datetime.get_date()
        )
        
        if not weather or 'main' not in weather or len(weather['main']) == 0:
            if not self._enabled:
                return
            elif self._missed_weather > 10:
                import microcontroller
                # restart the device

                self._weather_display.add_scroll_text("Restarting device")
                self._weather_display.show()
                microcontroller.reset()
                return
            else:
                self._missed_weather += 1
                self._weather_display.show() #TODO: is this required?
                return
            
        else:
            self._missed_weather = 0

        try:
            print('weather', weather)
            #self._weather_display.set_icon(weather["weather"][0]["icon"])
            self._apply_reading(('weather', 0, 'icon'), weather, self._weather_display.set_icon)

            #self._weather_display.set_temperature(str(weather["main"]["temp"]))
            self._apply_reading(('main', 'temp'), weather, self._weather_display.set_temperature)
            # add Scrolling items
            # TODO: These should really be a list of items that can be added and tracked easier.
            self._apply_reading(('main', 'humidity'), weather, self._weather_display.add_scroll_text)
            #self._weather_display.set_humidity(weather["main"]["humidity"])
            self._apply_reading(('main', 'feels_like'), weather, self._weather_display.add_scroll_text)
            #self._weather_display.set_feels_like(weather["main"]["feels_like"])
            self._apply_reading(('wind', 'speed'), weather, self._weather_display.add_scroll_text)
            #self._weather_display.set_wind(weather["wind"]["speed"])
            self._apply_reading(('weather', 0, 'description'), weather, self._weather_display.add_scroll_text)
            #self._weather_display.set_description(weather["weather"][0]["description"])
        except Exception as e:
            print('Unable to display weather', e)
        finally:
            self._weather_display.show()


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


    def scroll_label(self, key_input) -> None:
        self._weather_display.scroll_label(key_input)


    def weather_complete(self) -> bool:
        return not self._weather_display.scroll_queue
    
    def display_off(self) -> None:
        self._datetime.is_display_on = False
