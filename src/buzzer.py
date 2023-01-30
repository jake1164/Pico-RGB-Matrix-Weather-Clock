import board
from digitalio import DigitalInOut, Direction


class Buzzer:
    def __init__(self) -> None:
        """ Setup the buzzer and initate values stored by class """
        self._buzzer = DigitalInOut(board.GP27)
        self._buzzer.direction = Direction.OUTPUT
        self.enabled = True

        self._start_beep = False
        self.beep_count = 0


    def enable_buzzer(self, enable_buzzer):
        """ Enable or disable the buzzing """
        self.enabled = enable_buzzer


    def toggle_enable_buzzer(self):
        """ Toggle the buzzer enabled state """
        self.enable_buzzer(not self.enabled)


    def buzzer_start(self):
        """ Start the buzzing sound """
        self._buzzer.value = True


    def buzzer_stop(self):
        """ Stop the buzzing sound """
        self._buzzer.value = False

    def judgment_buzzer_switch(self):    
        if self.enabled and self._start_beep:
            self.buzzer_start()
        self._start_beep = True

    def three_beep(self):
        """ beep over the cource of 3 ticks """
        if self._start_beep:
            self.judgment_buzzer_switch()
            self.beep_count += 1
            if self.beep_count == 3:
                self.buzzer_stop()
                self.beep_count = 0
                self._start_beep = False
