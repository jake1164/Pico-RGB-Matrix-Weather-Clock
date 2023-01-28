import board
import digitalio
from driver_buzzer import Buzzer
from date_utils import get_max_day

class KeyProcessing:
    """ Key processing is all handled with the KeyProcessing class
    """
    def __init__(self, display_subsystem, light_sensor, time_format) -> None:
        """ 
            Initiates the keys used by the board. 
            Might move these to variables to 
        """
        _KEYPRESS_PINS = [board.GP15, board.GP19, board.GP21]
        # TODO: Remove display requirement and just return values that get passed to display. 
        self._display_subsystem = display_subsystem
        self._KEY_MENU = 0
        self._KEY_DOWN = 1
        self._KEY_UP = 2
        self._key_menu_value = 0
        self._key_down_value = 0
        self._key_up_value = 0
        self._key_pin_array = []

        # used outside of this class??
        self.page_id = 0
        self.time_setting_label = 0
        self.time_temp = [0, 0, 0]  # hour,min,sec
        self.date_temp = [0, 0, 0]  # year,mon,mday
        self.select_setting_options = 0

        ### These need to be moved to a settings class instead of mixed in here.
        self.timeFormatFlag = time_format # 12 or 24 (0 or 1) hour display.

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
            self._display_subsystem.setDateTime(self.select_setting_options, self.date_temp, self.time_temp)
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
                    self.time_temp[0] -= 1
                    if self.time_temp[0] < 0:
                        self.time_temp[0] = 23
                elif self.time_setting_label == 1:
                    self.time_temp[1] -= 1
                    if self.time_temp[1] < 0:
                        self.time_temp[1] = 59
                else:
                    self.time_temp[2] -= 1
                    if self.time_temp[2] < 0:
                        self.time_temp[2] = 59
            if self.select_setting_options == 1:
                if self.time_setting_label == 0:
                    self.date_temp[0] -= 1
                    if self.date_temp[0] < 2000:
                        self.date_temp[0] = 2099
                elif self.time_setting_label == 1:
                    self.date_temp[1] -= 1
                    if self.date_temp[1] < 1:
                        self.date_temp[1] = 12
                else:
                    self.date_temp[2] -= 1
                    if self.date_temp[2] < 1:
                        self.date_temp[2] = get_max_day(self.date_temp[1], self.date_temp[0])
            if self.select_setting_options == 2:                
                self._buzzer.toggle_enable_buzzer()
                #if beepFlag:
                #    beepFlag = 0
                #else:
                #    beepFlag = 1
            if self.select_setting_options == 3:
                self._light_sensor.toggle_auto_dimming()
            if self.select_setting_options == 4:
                if self.timeFormatFlag:
                    self.timeFormatFlag = 0 # 12 hour
                else:
                    self.timeFormatFlag = 1 # 24 hour
                self._display_subsystem.setTimeFormat(self.timeFormatFlag)


    def key_up_processing_function(self):
        if self.page_id == 1:
            self.select_setting_options += 1
            if self.select_setting_options == 5:
                self.select_setting_options = 0
        if self.page_id == 2:
            if self.select_setting_options == 0:
                if self.time_setting_label == 0:
                    self.time_temp[0] += 1
                    if self.time_temp[0] == 24:
                        self.time_temp[0] = 0
                elif self.time_setting_label == 1:
                    self.time_temp[1] += 1
                    if self.time_temp[1] == 60:
                        self.time_temp[1] = 0
                else:
                    self.time_temp[2] += 1
                    if self.time_temp[2] == 60:
                        self.time_temp[2] = 0
            if self.select_setting_options == 1:
                if self.time_setting_label == 0:
                    self.date_temp[0] += 1
                    if self.date_temp[0] > 2099:
                        self.date_temp[0] = 2000
                elif self.time_setting_label == 1:
                    self.date_temp[1] += 1
                    if self.date_temp[1] > 12:
                        self.date_temp[1] = 1
                else:
                    self.date_temp[2] += 1
                    if self.date_temp[2] > get_max_day(self.date_temp[1], self.date_temp[0]):
                        self.date_temp[2] = 1
            if self.select_setting_options == 2:
                self._buzzer.toggle_enable_buzzer()
                #if beepFlag:
                #    beepFlag = 0
                #else:
                #    beepFlag = 1
            if self.select_setting_options == 3:
                self._light_sensor.toggle_auto_dimming()
            if self.select_setting_options == 4:
                if self.timeFormatFlag:
                    self.timeFormatFlag = 0 # 12 hour
                else:
                    self.timeFormatFlag = 1 # 24 hour
                #showSystem.setTimeFormat(timeFormatFlag)            
                self._display_subsystem.setTimeFormat(self.timeFormatFlag)