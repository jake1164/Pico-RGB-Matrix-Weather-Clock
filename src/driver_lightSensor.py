import board
from analogio import AnalogIn

class LightSensor:
    def __init__(self, display) -> None:
        self.LIGHT_THRESHOLD = 2800 # Lower the value the brighter the light.
        #TODO: Remove display and just check if the light sensor is tripped or not.
        self._display = display
        self.auto_dimming = True
        self._analog_in = AnalogIn(board.GP26)


    def _get_voltage(self):
        """ returns the voltage of the light sensor """
        return int((self._analog_in.value * 3300) / 65536)


    def check_light_sensor(self):
        """ Get the voltag and if its above a threshold then turn the display off """
        if self.auto_dimming:
            light = self._get_voltage()
            if light > self.LIGHT_THRESHOLD:
                self._display.brightness = 0.0
            else:
                self._display.brightness = 0.1

    def toggle_auto_dimming(self):
        self.auto_dimming = not self.auto_dimming