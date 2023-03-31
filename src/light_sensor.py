import board
from analogio import AnalogIn

class LightSensor:
    def __init__(self, settings) -> None:
        self.LIGHT_THRESHOLD = 2800 # Lower the value the brighter the light.
        self._settings = settings
        self._analog_in = AnalogIn(board.GP26)        
        self.dark_mode = False 


    def _get_voltage(self):
        """ returns the voltage of the light sensor """
        return int((self._analog_in.value * 3300) / 65536)


    def get_display_mode(self):
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

        return self.dark_mode