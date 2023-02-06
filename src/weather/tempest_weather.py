# Pulls weather from a the weatherflow api (from a tempest weather station) 
# https://weatherflow.github.io/Tempest/api/ 
import os

STATIONS_URL = 'https://swd.weatherflow.com/swd/rest/stations?token={}'
URL = 'http://swd.weatherflow.com/swd/rest/observations/station/{}?token={}'
BETTER_URL = 'https://swd.weatherflow.com/swd/rest/better_forecast?station_id={}&units_temp=f&units_wind=mph&units_pressure=mmhg&units_precip=in&units_distance=mi&token={}'

class TempestWeather():
    def __init__(self, network) -> None:
        self.network = network
        token = os.getenv('TEMPEST_API_TOKEN')
        station = os.getenv('TEMPEST_STATION')
        self._url = URL.format(station, token)

    def get_weather(self):
        weather = self.network.getJson(self._url)
        print(weather)
    
    def get_update_interval(self):
        """ Returns the weather update interval in seconds """
        return 20