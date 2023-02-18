from . import tempest_weather, open_weather

def Factory(api, weather_display, datetime, network):
    
    apis = {
        "OWM": open_weather.OpenWeather,
        "TEMPEST": tempest_weather.TempestWeather
    }

    if(api == "OWM"):
        primary = apis["OWM"](network, weather_display.units)
        return Weather({ "PRIMARY": primary }, weather_display, datetime)
    elif (api == "TEMPEST"):
        primary = apis["TEMPEST"](network, weather_display.units)
        secondary = apis["OWM"](network, weather_display.units)
        return Weather({ "PRIMARY": primary, "SECONDARY": secondary }, weather_display, datetime)


class Weather():    
    ''' Weather takes a primary and secondary weather api. '''
    def __init__(self, apis, weather_display, datetime) -> None:
        self.SKIP_SECONDARY = 4 # Skip this many times between updates
        self._datetime = datetime
        self._display = weather_display
        self._primary = apis['PRIMARY']
        self._secondary = apis['SECONDARY'] if len(apis) == 2 else None
        self.skip = 0

    def show_weather(self):        
        self._primary.show_weather(self._display)        
        if self._secondary and self.skip == 0: #TODO reduce the frequency of secondary calls
            self.skip = self.SKIP_SECONDARY
            self._secondary.show_secondary(self._display)
        elif self._secondary:
            self.skip -= 1

    def show_datetime(self):
        self._display.set_time(self._datetime.get_time())
        self._display.set_date(
            self._datetime.get_date()
        )        


    def get_update_interval(self):
        return self._primary.get_update_interval()


    def scroll_label(self):
        self._display.scroll_label()


