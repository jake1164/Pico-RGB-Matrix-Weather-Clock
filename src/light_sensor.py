import board
from analogio import AnalogIn

class LightSensor:
    def __init__(self, settings, display) -> None:
        self.LIGHT_THRESHOLD = 2800 # Lower the value the brighter the light.
        self._settings = settings
        self._display = display
        self._analog_in = AnalogIn(board.GP26)        
        self.dark_mode = False 
        #self.display_off = False # if darkmode && <

        self._dimming = False # TODO remove me


    def _get_voltage(self):
        """ returns the voltage of the light sensor """
        return int((self._analog_in.value * 3300) / 65536)


    def is_dimming(self): # Access display_off directly.
        return self._dimming

    def check_light_sensor1(self):
        if self._settings.dark_mode:
            light = self._get_voltage()
            if not self.dark_mode and light > self._settings.night_level:
                self.dark_mode = True
            elif self.dark_mode and (light > self._settings.night_level - 100):
                self.dark_mode = True
            else:
                self.dark_mode = False
        else:
            self.dark_mode = False

    def check_light_sensor(self):
        """ Get the voltag and if its above a threshold then turn the display off """
        if self._settings.autodim:
            # TODO: need to do some sort of debouncing here. 
            light = self._get_voltage()
            if not self._dimming and light > self.LIGHT_THRESHOLD:
                self._dimming = True                
            if self._dimming and (light > self.LIGHT_THRESHOLD - 200):
                self._dimming = True
            else:
                self._dimming = False

            self._set_dimming()    


    def _set_dimming(self):
        if self._dimming:
            self._display.brightness = 0.0
        else:
            self._display.brightness = 0.1