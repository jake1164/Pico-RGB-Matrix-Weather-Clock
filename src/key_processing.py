import time
import board
import digitalio
from settings_display import SETTINGS

# Define key pin constants for clarity
KEY_0, KEY_1, KEY_2 = board.GP15, board.GP19, board.GP21

class KeyProcessing:
    """ Key processing is all handled with the KeyProcessing class
    """
    def __init__(self, settings, date_processing, buzzer) -> None:
        """ Initiates the keys used by the board.
        """
        _KEYPRESS_PINS = [KEY_0, KEY_1, KEY_2]
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
        self._long_press_threshold = 20  # Threshold for long press detection
        self._long_press_triggered = False  # Flag to prevent processing key release after long press

        # used outside of this class
        self.page_id = 0
        self.time_setting_label = 0
        self.select_setting_options = 0

        # Initialize other methods
        self._key_init(_KEYPRESS_PINS)


    def _key_init(self, pins) -> None:
        """ We initialize multiple buttons to listen to,
            pass in the pins they listen on and we will
            initialize them all here.
        """
        for pin in pins:
            key_pin =digitalio.DigitalInOut(pin)
            key_pin.direction = digitalio.Direction.INPUT
            key_pin.pull = digitalio.Pull.UP
            self._key_pin_array.append(key_pin)


    def get_key_value(self) -> int:
        """ When one of the buttons has been pressed it is identified here
            The value is return identifiying which key was pressed. 
        """
        for key_pin in self._key_pin_array:
            if not key_pin.value:
                key_value = self._key_pin_array.index(key_pin)
                return key_value


    def key_processing(self, keyValue) -> None:
        """ When a value is passed in this function will interperate the button press.
        """
        # Increment counters when buttons are pressed
        if keyValue == self._KEY_MENU:
            self._key_menu_value += 1
        if keyValue == self._KEY_DOWN:
            self._key_down_value += 1
        if keyValue == self._KEY_UP:
            self._key_up_value += 1

        # Only beep when a key is actually pressed (not when keyValue is None)
        if keyValue is not None:
            self._buzzer.three_beep() # Short beep that a key press was made

        #print(f'key_processing - key: {keyValue} menu: {self._key_menu_value}')

        # Check for long press on any key while in settings (page_id > 0)
        # Exit immediately when threshold is reached, even while button is still held
        if self.page_id > 0 and not self._long_press_triggered:
            if self._key_menu_value >= self._long_press_threshold or self._key_down_value >= self._long_press_threshold or self._key_up_value >= self._long_press_threshold:
                self.key_exit_processing_function()
                self._buzzer.judgment_buzzer_switch()
                # Set flag to prevent processing the key release AND prevent retriggering
                self._long_press_triggered = True
                # Don't reset counters yet - let them reset on key release
                return  # Exit early to prevent further processing

        # If long press was triggered, wait for button to be fully released before allowing any action
        if self._long_press_triggered:
            # Check if button is released
            if keyValue is None:
                # Reset all counters
                self._key_menu_value = 0
                self._key_down_value = 0
                self._key_up_value = 0
                self._long_press_triggered = False
            return  # Don't process anything while flag is set

        # I think the premise is they wait for none to tell if the key has been released, but it only really relates to key 3
        # Without the None key it will keypress twice. 
        # Menu key should work for any duration of press
        if self._key_menu_value > 0 and keyValue is None:
            self.key_menu_processing_function()
            self._buzzer.judgment_buzzer_switch() # When the menu exits it beeps also
            self._key_menu_value = 0

        if self._key_down_value > 0 and self._key_down_value < self._long_press_threshold and keyValue is None:
            self.key_press_processing(up_key=False)
            self._buzzer.judgment_buzzer_switch()
            self._key_down_value = 0
        elif self._key_down_value >= self._long_press_threshold and keyValue is None:
            self._key_down_value = 0

        if self._key_up_value > 0 and self._key_up_value < self._long_press_threshold and keyValue is None:
            self.key_press_processing(up_key=True)
            self._buzzer.judgment_buzzer_switch()
            self._key_up_value = 0
        elif self._key_up_value >= self._long_press_threshold and keyValue is None:
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


    def key_menu_processing_function(self) -> None:
        if self.page_id == 2 and self.select_setting_options <= 1:
            self.time_setting_label += 1
            if self.time_setting_label > 2:
                self.time_setting_label = 0
        self.page_id += 1
        if self.page_id > 2:
            self.page_id = 2


    def key_press_processing(self, up_key) -> None:
        if self.page_id == 1:
            self.select_setting_options = self.select_setting_options + 1 if up_key else self.select_setting_options - 1
            if self.select_setting_options == -1:
                self.select_setting_options = len(SETTINGS) - 1
            elif self.select_setting_options == len(SETTINGS):
                self.select_setting_options = 0
        if self.page_id == 2:
            if self.select_setting_options == 0: # TIME SETTING 
                self._settings.ntp_enabled = False
                if self.time_setting_label == 0:
                    self._datetime.set_hour(up_key) # decrement
                elif self.time_setting_label == 1:
                    self._datetime.set_min(up_key)
                else: #TODO: Remove seconds and just set hour/ min
                    self._datetime.set_sec(up_key)
            if self.select_setting_options == 1: # DATE SETTING
                self._settings.ntp_enabled = False
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
                # If NTP is disabled, manually adjust the RTC time by +/- 1 hour
                if not self._settings.ntp_enabled:
                    current_time = self._datetime.rtc.datetime
                    time_list = list(current_time)
                    if self._settings.dst_adjust:
                        # DST turned ON: add 1 hour
                        time_list[3] = (time_list[3] + 1) % 24
                    else:
                        # DST turned OFF: subtract 1 hour
                        time_list[3] = (time_list[3] - 1) % 24
                    self._datetime.rtc.datetime = time.struct_time(tuple(time_list))
                else:
                    # If NTP is enabled, trigger update from NTP on next exit
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
            if self.select_setting_options == 10: # NTP ON / OFF
                self._settings.ntp_enabled = not self._settings.ntp_enabled
                # Force the time to be synced.
                if self._settings.ntp_enabled:
                    self._dst_adjusted = True
