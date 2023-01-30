import adafruit_display_text.label
from date_utils import *


class DISPLAYSUBSYSTEM:
    def __init__(self, datetime_processing):
        self._first_enter_page = True
        self._datetime = datetime_processing


    def showDateTimePage(self,line1,line2,line3):
        line1.x = 2
        line1.y = 5
        line2.x = 8
        line2.y = 15
        line3.x = 10
        line3.y = 25
        date_string = self._datetime.get_date()
        time_string = self._datetime.get_time()
        dow = self._datetime.get_dow()
        line1.text = date_string
        line2.text = time_string
        line3.text= dow


    def showSetListPage(self,line1,line2,_selectSettingOptions):
        line1.x = 8
        line1.y = 7
        line2.x = 8
        line2.y = 23
        line1.text = "SET LIST"
        if _selectSettingOptions == 0:
            line2.text = "TIME SET"
        if _selectSettingOptions == 1:
            line2.text = "DATE SET"
        if _selectSettingOptions == 2:
            line2.text = "BEEP SET"
        if _selectSettingOptions == 3:
            line2.text = "AUTODIM"
        if _selectSettingOptions == 4:
            line2.text = "12/24 HR"            
        if not self._first_enter_page:
            self._first_enter_page = True
            

    def timeSettingPage(self,line2,line3,_timeSettingLabel):
        update = False
        if self._first_enter_page:
            line2.x = 8
            line2.y = 13
            update = True
            self._first_enter_page = False
        line2.text = self._datetime.get_setting_time(update)
        line3.text = "^"
        if _timeSettingLabel == 0:
            line3.x = 12
            line3.y = 24
        elif _timeSettingLabel == 1:
            line3.x = 29
            line3.y = 24
        else:
            line3.x = 47
            line3.y = 24


    def dateSettingPage(self, line2, line3, _timeSettingLabel):
        update = False
        if self._first_enter_page:
            update = True
            line2.x = 3
            line2.y = 13
            self._first_enter_page = False
        line2.text = self._datetime.get_setting_date(update)
        line3.text = "^"
        if _timeSettingLabel == 0:
            line3.x = 12
            line3.y = 24
        elif _timeSettingLabel == 1:
            line3.x = 36
            line3.y = 24
        else:
            line3.x = 54
            line3.y = 24
            

    def onOffPage(self,line2,line3,_selectSettingOptions,_beepFlag,_autoLightFlag):
        if _selectSettingOptions == 2:
            line2.x = 20
            line2.y = 7
            line3.x = 20
            line3.y = 23
            if _beepFlag:
                line2.text = "> on"
                line3.text = "  off"
            else:
                line2.text = "  on"
                line3.text = "> off"
        if _selectSettingOptions == 3:
            line2.x = 20
            line2.y = 7
            line3.x = 20
            line3.y = 23
            
            if _autoLightFlag:
                line2.text = "> on"
                line3.text = "  off"
            else:
                line2.text = "  on"
                line3.text = "> off"
        if _selectSettingOptions == 4:
            line2.x = 10
            line2.y = 7
            line3.x = 10
            line3.y = 23            
            if self._datetime.is_12hr():
                line2.text = "> 12 Hr"
                line3.text = "  24 Hr"
            else:
                line2.text = "  12 Hr"
                line3.text = "> 24 Hr"                          