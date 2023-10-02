import gc
import terminalio
import displayio
from adafruit_display_text import bitmap_label

SETTINGS = [
    {
        "text": "TIME SET",
        "type": "set_time"
    },    
    {
        "text": "DATE SET",
        "type": "set_date"
    },
    {
        "text": "BEEP SET",
        "type": "bool"
    },
    {
        "text": "AUTODIM",
        "type": "bool"
    },
    {
        "text": "12/24 HR",
        "type": "bool"
    },
    {
        "text": "APPLY DST",
        "type": "bool"
    },
    {
        "text": "DARK MODE",
        "type": "bool"
    },
    {
        "text": "DM LEVEL",
        "type": "number"
    },
    {
        "text": "TIME ON",
        "type": "time"
    },
    {
        "text": "TIME OFF",
        "type": "time"
    },
    {
        "text": "NTP ON",
        "type": "bool"
    }
    ]


class SettingsDisplay(displayio.Group):
    def __init__(self, display, datetime_processing):
        super().__init__()
        display.rotation = 0
        self.display = display
        self._first_enter_page = True
        self._datetime = datetime_processing

        line1 = bitmap_label.Label(terminalio.FONT, color=0x00DD00)
        line2 = bitmap_label.Label(terminalio.FONT, color=0x00DDDD)
        line3 = bitmap_label.Label(terminalio.FONT, color=0x0000DD)
        line3.x = 12
        line3.y = 56

        self._line1 = line1
        self._line2 = line2
        self._line3 = line3

        self._line_group = displayio.Group()
        self._line_group.append(self)
        self.append(self._line1)
        self.append(self._line2)
        self.append(self._line3)    


    def showSetListPage(self, selectSettingOptions):
        self._line3.text = ""

        self._line1.text = "SET LIST"
        self._line1.x = 8
        self._line1.y = 7

        self._line2.text = SETTINGS[selectSettingOptions]["text"]
        #self._line2.x = 8
        self._line2.x = self._get_x_position(self._line2.text)
        self._line2.y = 23
            
        if not self._first_enter_page:
            self._first_enter_page = True
        self.display.show(self._line_group)


    def timeSettingPage(self, timeSettingLabel):
        self._line1.text = ""
        update = False
        if self._first_enter_page:
            self._line2.x = 8
            self._line2.y = 13
            update = True
            self._first_enter_page = False
        self._line2.text = self._datetime.get_setting_time(update)
        self._line3.text = "^"
        if timeSettingLabel == 0:
            self._line3.x = 12
            self._line3.y = 24
        elif timeSettingLabel == 1:
            self._line3.x = 29
            self._line3.y = 24
        else:
            self._line3.x = 47
            self._line3.y = 24
        self.display.show(self._line_group)


    def time_page(self, setting_text, setting_time):
        ''' 
        Eventual replacement time. 
        '''
        self._line1.text = setting_text
        if self._first_enter_page:
            self._line2.x = 18
            self._line2.y = 18
            self._first_enter_page = False
 
        self._line2.text = f"{setting_time:02d}:00"
        self._line3.text = "^"
        self._line3.x = 21
        self._line3.y = 28
        self.display.show(self._line_group)


    def dateSettingPage(self, timeSettingLabel):
        self._line1.text = ""
        update = False
        if self._first_enter_page:
            update = True
            self._line2.x = 3
            self._line2.y = 13
            self._first_enter_page = False
        self._line2.text = self._datetime.get_setting_date(update)
        self._line3.text = "^"
        if timeSettingLabel == 0:
            self._line3.x = 12
            self._line3.y = 24
        elif timeSettingLabel == 1:
            self._line3.x = 36
            self._line3.y = 24
        else:
            self._line3.x = 54
            self._line3.y = 24
        self.display.show(self._line_group)
            

    def onOffPage(self, selectSettingOptions, settings):
        self._line1.text = ""
        if selectSettingOptions == 2: # BEEP
            self._line2.x = 20
            self._line2.y = 7
            self._line3.x = 20
            self._line3.y = 23
            if settings.beep:
                self._line2.text = "> on"
                self._line3.text = "  off"
            else:
                self._line2.text = "  on"
                self._line3.text = "> off"
        if selectSettingOptions == 3: # AUTODIM
            self._line2.x = 20
            self._line2.y = 7
            self._line3.x = 20
            self._line3.y = 23
            
            if settings.autodim:
                self._line2.text = "> on"
                self._line3.text = "  off"
            else:
                self._line2.text = "  on"
                self._line3.text = "> off"
        if selectSettingOptions == 4: # 12/24 HR
            self._line2.x = 10
            self._line2.y = 7
            self._line3.x = 10
            self._line3.y = 23            
            if self._datetime.is_12hr():
                self._line2.text = "> 12 Hr"
                self._line3.text = "  24 Hr"
            else:
                self._line2.text = "  12 Hr"
                self._line3.text = "> 24 Hr"
        if selectSettingOptions == 5: # DST ADJUST
            self._line2.x = 20
            self._line2.y = 7
            self._line3.x = 20
            self._line3.y = 23
            
            if settings.dst_adjust:
                self._line2.text = "> on"
                self._line3.text = "  off"
            else:
                self._line2.text = "  on"
                self._line3.text = "> off" 
        if selectSettingOptions == 6: # DARK MODE
            self._line2.x = 20
            self._line2.y = 7
            self._line3.x = 20
            self._line3.y = 23
            
            if settings.dark_mode:
                self._line2.text = "> on"
                self._line3.text = "  off"
            else:
                self._line2.text = "  on"
                self._line3.text = "> off"                 
        if selectSettingOptions == 10: # NTP ENABLED
            self._line2.x = 20
            self._line2.y = 7
            self._line3.x = 20
            self._line3.y = 23
            
            if settings.ntp_enabled:
                self._line2.text = "> on"
                self._line3.text = "  off"
            else:
                self._line2.text = "  on"
                self._line3.text = "> off"
        self.display.show(self._line_group)


    def number_display_page(self, settings):
        '''
        Display a number to be incremented / decremented
        '''
        self._line1.text = "DM Level"

        self._line2.x = 20
        self._line2.y = 18
        self._line2.text = str(settings.night_level)
        self._line3.text = "^"

        self._line3.x = 29
        self._line3.y = 28

        self.display.show(self._line_group)


    def _get_x_position(self, text) -> int:
        '''
        Each digit has a length of 6 so return the padding required on the left to center it.
        '''
        size = len(text)
        if size > 9 or size == 0:
            return 1
        
        return int((64 - (size * 6)) / 2)