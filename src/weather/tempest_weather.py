# Pulls weather from a the weatherflow api (from a tempest weather station) 
# https://weatherflow.github.io/Tempest/api/ 
import os

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
        try:
            weather = self.get_weather()
        except Exception as ex:
            print('unable to get weather', ex)
            weather = None

        if weather == {} or weather['obs'] == None or len(weather['obs']) == 0:
            weather_display.show()
            return

        try:                
            if 'air_temperature' in weather['obs'][0].keys():
                weather_display.set_temperature(self._convert_temperature(weather["obs"][0]["air_temperature"]))

            if 'relative_humidity' in weather['obs'][0].keys():
                weather_display.set_humidity(weather["obs"][0]["relative_humidity"])
            if "feels_like" in weather["obs"][0].keys():
                weather_display.set_feels_like(self._convert_temperature(weather["obs"][0]["feels_like"]))
            if 'wind_avg' in weather['obs'][0].keys():
                weather_display.set_wind(self._convert_windspeed(weather["obs"][0]["wind_avg"]))
        except Exception as ex:
            print('Unable to display weather', ex)
        finally:        
            weather_display.show()


    def _get_reading(self, field, weather):
        if(field in weather['obs'][0].keys()):
            return weather['obs'][0][field]
        return None

    def _convert_temperature(self, celsius):
        if self._units == "imperial":
            return (celsius * 1.8) + 32
        return celsius


    def _convert_windspeed(self, speed):
        if self._units == "imperal":
            return speed * 2.23693629
        return speed