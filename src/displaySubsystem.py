import terminalio
import displayio
import adafruit_display_text.label
from date_utils import *


class DisplaySubsystem(displayio.Group):
    def __init__(self, display, datetime_processing):
        super().__init__()
        display.rotation = 0
        self.display = display
        self._first_enter_page = True
        self._datetime = datetime_processing

        line1 = adafruit_display_text.label.Label(terminalio.FONT, color=0x00DD00)
        line2 = adafruit_display_text.label.Label(terminalio.FONT, color=0x00DDDD)
        line3 = adafruit_display_text.label.Label(terminalio.FONT, color=0x0000DD)
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

    def showDateTimePage(self):
        self._line1.x = 2
        self._line1.y = 5
        self._line2.x = 8
        self._line2.y = 15
        self._line3.x = 10
        self._line3.y = 25
        date_string = self._datetime.get_date()
        time_string = self._datetime.get_time()
        dow = self._datetime.get_dow()
        self._line1.text = date_string
        self._line2.text = time_string
        self._line3.text= dow


    def showSetListPage(self, selectSettingOptions):
        self._line3.text = ""
        self._line1.x = 8
        self._line1.y = 7
        self._line2.x = 8
        self._line2.y = 23
        self._line1.text = "SET LIST"
        if selectSettingOptions == 0:
            self._line2.text = "TIME SET"
        if selectSettingOptions == 1:
            self._line2.text = "DATE SET"
        if selectSettingOptions == 2:
            self._line2.text = "BEEP SET"
        if selectSettingOptions == 3:
            self._line2.text = "AUTODIM"
        if selectSettingOptions == 4:
            self._line2.text = "12/24 HR"            
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
            

    def onOffPage(self, selectSettingOptions, beepFlag, autoLightFlag):
        self._line1.text = ""
        if selectSettingOptions == 2:
            self._line2.x = 20
            self._line2.y = 7
            self._line3.x = 20
            self._line3.y = 23
            if beepFlag:
                self._line2.text = "> on"
                self._line3.text = "  off"
            else:
                self._line2.text = "  on"
                self._line3.text = "> off"
        if selectSettingOptions == 3:
            self._line2.x = 20
            self._line2.y = 7
            self._line3.x = 20
            self._line3.y = 23
            
            if autoLightFlag:
                self._line2.text = "> on"
                self._line3.text = "  off"
            else:
                self._line2.text = "  on"
                self._line3.text = "> off"
        if selectSettingOptions == 4:
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
        self.display.show(self._line_group)