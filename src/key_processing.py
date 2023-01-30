import board
import digitalio
from buzzer import Buzzer

class KeyProcessing:
    """ Key processing is all handled with the KeyProcessing class
    """
    def __init__(self, light_sensor, date_processing) -> None:
        """ 
            Initiates the keys used by the board. 
            Might move these to variables to 
        """
        _KEYPRESS_PINS = [board.GP15, board.GP19, board.GP21]
        self._KEY_MENU = 0
        self._KEY_DOWN = 1
        self._KEY_UP = 2
        self._key_menu_value = 0
        self._key_down_value = 0
        self._key_up_value = 0
        self._key_pin_array = []
        self._datetime = date_processing

        # used outside of this class
        self.page_id = 0
        self.time_setting_label = 0
        self.select_setting_options = 0

        # Initialize other methods
        self._buzzer = Buzzer()
        self._light_sensor = light_sensor 
        self._key_init(_KEYPRESS_PINS)


    def _key_init(self, pins):
        for pin in pins:
            key_pin =digitalio.DigitalInOut(pin)
            key_pin.direction = digitalio.Direction.INPUT
            key_pin.pull = digitalio.Pull.UP
            self._key_pin_array.append(key_pin)    


    def get_key_value(self):
        for key_pin in self._key_pin_array:
            if not key_pin.value:
                key_value = self._key_pin_array.index(key_pin)
                return key_value


    def key_processing(self, keyValue):        
        if keyValue == self._KEY_MENU:
            self._key_menu_value += 1
        if keyValue == self._KEY_DOWN:
            self._key_down_value += 1
        if keyValue == self._KEY_UP:
            self._key_up_value += 1

        self._buzzer.three_beep() # Short beep that a key press was made

        if self._key_menu_value > 0 and self._key_menu_value < 20 and keyValue == None:
            self.key_menu_processing_function()
            self._buzzer.judgment_buzzer_switch() # When the menu exits it beeps also
            self._key_menu_value = 0
        elif self._key_menu_value >= 20 and keyValue == None:
            self._key_menu_value = 0

        if self._key_down_value > 0 and self._key_down_value < 20 and keyValue == None:
            self.key_down_processing_function()
            self._buzzer.judgment_buzzer_switch()
            self._key_down_value = 0
        elif self._key_down_value >= 20 and keyValue == None:
            self._key_down_value = 0

        if self._key_up_value > 0 and self._key_up_value < 20 and keyValue == None:
            self.key_up_processing_function()
            self._buzzer.judgment_buzzer_switch()
            self._key_up_value = 0
        elif self._key_up_value >= 20 and keyValue == None:
            self.key_exit_processing_function()
            self._buzzer.judgment_buzzer_switch()
            self._key_up_value = 0

    def key_exit_processing_function(self):
        if self.page_id == 2 and self.select_setting_options <= 1:
            self._datetime.set_datetime(self.select_setting_options)
            self.time_setting_label = 0
        self.page_id -= 1
        if self.page_id < 0:
            self.page_id = 0            


    def key_menu_processing_function(self):
        if self.page_id == 2 and self.select_setting_options <= 1:
            self.time_setting_label += 1
            if self.time_setting_label > 2:
                self.time_setting_label = 0
        self.page_id += 1
        if self.page_id > 2:
            self.page_id = 2


    def key_down_processing_function(self):
        if self.page_id == 1:
            self.select_setting_options -= 1
            if self.select_setting_options == -1:
                self.select_setting_options = 4
        if self.page_id == 2:
            if self.select_setting_options == 0:
                if self.time_setting_label == 0:
                    self._datetime.set_hour(False) # decrement
                elif self.time_setting_label == 1:
                    self._datetime.set_min(False)
                else:
                    self._datetime.set_sec(False)
            if self.select_setting_options == 1:
                if self.time_setting_label == 0:
                    self._datetime.set_year(False)
                elif self.time_setting_label == 1:
                    self._datetime.set_month(False)
                else:
                    self._datetime.set_day(False)
            if self.select_setting_options == 2:                
                self._buzzer.toggle_enable_buzzer()
            if self.select_setting_options == 3:
                self._light_sensor.toggle_auto_dimming()
            if self.select_setting_options == 4:
                self._datetime.toggle_time_format()


    def key_up_processing_function(self):
        if self.page_id == 1:
            self.select_setting_options += 1
            if self.select_setting_options == 5:
                self.select_setting_options = 0
        if self.page_id == 2:
            if self.select_setting_options == 0:
                if self.time_setting_label == 0:
                    self._datetime.set_hour(True) # increment                    
                elif self.time_setting_label == 1:
                    self._datetime.set_min(True)
                else:
                    self._datetime.set_sec(True)
            if self.select_setting_options == 1:
                if self.time_setting_label == 0:
                    self._datetime.set_year(True)
                elif self.time_setting_label == 1:
                    self._datetime.set_month(True)
                else:
                    self._datetime.set_day(True)
            if self.select_setting_options == 2:
                self._buzzer.toggle_enable_buzzer()
            if self.select_setting_options == 3:
                self._light_sensor.toggle_auto_dimming()
            if self.select_setting_options == 4:
                self._datetime.toggle_time_format()