import board
import digitalio
from displaySubsystem import SETTINGS

class KeyProcessing:
    """ Key processing is all handled with the KeyProcessing class
    """
    def __init__(self, settings, date_processing, buzzer) -> None:
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
        self._settings = settings
        self._buzzer = buzzer
        self._dst_adjusted = False
        self._dst_setting = self._settings.dst_adjust

        # used outside of this class
        self.page_id = 0
        self.time_setting_label = 0
        self.select_setting_options = 0

        # Initialize other methods        
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
        #print(f'key_processing - key: {keyValue} menu: {self._key_menu_value}')

        # I think the premise is they wait for none to tell if the key has been released, but it only really relates to key 3
        # Without the None key it will keypress twice. 
        #if self._key_menu_value > 0 and self._key_menu_value < 20 and keyValue == None:        
        if self._key_menu_value > 0 and keyValue == None:        
            self.key_menu_processing_function()
            self._buzzer.judgment_buzzer_switch() # When the menu exits it beeps also
            self._key_menu_value = 0
        elif self._key_menu_value >= 20 and keyValue == None:
            self._key_menu_value = 0

        if self._key_down_value > 0 and self._key_down_value < 20 and keyValue == None:
            self.key_press_processing(up_key=False)
            self._buzzer.judgment_buzzer_switch()
            self._key_down_value = 0
        elif self._key_down_value >= 20 and keyValue == None:
            self._key_down_value = 0

        if self._key_up_value > 0 and self._key_up_value < 20 and keyValue == None:
            self.key_press_processing(up_key=True)
            self._buzzer.judgment_buzzer_switch()
            self._key_up_value = 0
        elif self._key_up_value >= 20 and keyValue == None: # if keydown is >20 then would it exit for you?
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
        if self.page_id == 0:
            if self._dst_adjusted:
                self._datetime.update_from_ntp()
                self._dst_setting = self._settings.dst_adjust
                self._dst_adjusted = False
            self._settings.persist_settings()


    def key_menu_processing_function(self):
        if self.page_id == 2 and self.select_setting_options <= 1:
            self.time_setting_label += 1
            if self.time_setting_label > 2:
                self.time_setting_label = 0
        self.page_id += 1
        if self.page_id > 2:
            self.page_id = 2


    def key_press_processing(self, up_key):
        if self.page_id == 1:
            self.select_setting_options = self.select_setting_options + 1 if up_key else self.select_setting_options - 1
            if self.select_setting_options == -1:
                self.select_setting_options = len(SETTINGS) - 1
            elif self.select_setting_options == len(SETTINGS):
                self.select_setting_options = 0
        if self.page_id == 2:
            if self.select_setting_options == 0: # TIME SETTING 
                if self.time_setting_label == 0:
                    self._datetime.set_hour(up_key) # decrement
                elif self.time_setting_label == 1:
                    self._datetime.set_min(up_key)
                else: #TODO: Remove seconds and just set hour/ min
                    self._datetime.set_sec(up_key)
            if self.select_setting_options == 1: # DATE SETTING
                if self.time_setting_label == 0:
                    self._datetime.set_year(up_key)
                elif self.time_setting_label == 1:
                    self._datetime.set_month(up_key)
                else:
                    self._datetime.set_day(up_key)
            if self.select_setting_options == 2: # Buzzer Enable / Disable               
                self._settings.beep = not self._settings.beep
            if self.select_setting_options == 3: # Autodim (turn off screen)
                self._settings.autodim = not self._settings.autodim
            if self.select_setting_options == 4: # 12/24hr clock
                self._settings.twelve_hr = not self._settings.twelve_hr
            if self.select_setting_options == 5: # DST adjust
                self._settings.dst_adjust = not self._settings.dst_adjust
                self._dst_adjusted = True
            if self.select_setting_options == 6: # DARK MODE
                self._settings.dark_mode = not self._settings.dark_mode
            if self.select_setting_options == 7: # DARK MODE LEVEL
                level = 100 if up_key else -100
                self._settings.night_level = self._settings.night_level + level
            if self.select_setting_options == 8: # TIME ON
                # Display the time_on setting and incremnet the hour only
                adj = 1 if up_key else -1
                self._settings.on_time = self._settings.on_time + adj
            if self.select_setting_options == 9: # TIME OFF
                adj = 1 if up_key else -1
                self._settings.off_time = self._settings.off_time + adj