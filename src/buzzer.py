import board
from digitalio import DigitalInOut, Direction

# Buzzer pin constant
BUZZ_PIN = board.GP27


class Buzzer:
    def __init__(self, settings) -> None:
        """ Setup the buzzer and initiate values stored by class """
        self._buzzer = DigitalInOut(BUZZ_PIN)
        self._buzzer.direction = Direction.OUTPUT
        self._settings = settings
        self._beep_counter = 0
        self._beep_active = False


    def buzzer_start(self):
        """ Start the buzzing sound """
        self._buzzer.value = True


    def buzzer_stop(self):
        """ Stop the buzzing sound """
        self._buzzer.value = False

    def judgment_buzzer_switch(self):    
        """ Check if beeping is enabled and start a beep """
        if self._settings.beep:
            self._beep_active = True
            self._beep_counter = 0
            self.buzzer_start()

    def three_beep(self):
        """ Start a short beep (will last for 3 update cycles) """
        if self._settings.beep:
            self.judgment_buzzer_switch()

    def update(self):
        """ Update the buzzer state - should be called regularly in the main loop """
        if self._beep_active:
            self._beep_counter += 1
            if self._beep_counter >= 3:
                self.buzzer_stop()
                self._beep_active = False
                self._beep_counter = 0

    def is_beeping(self):
        """ Check if the buzzer is currently active """
        return self._beep_active and self._settings.beep
