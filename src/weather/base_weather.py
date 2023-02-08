import displayio
from terminalio import FONT
from adafruit_display_text.label import Label

class BaseDisplay(displayio.Group):
    def __init__(self,) -> None:
        super().__init__()
        self.root_group = displayio.Group()
        self.root_group.append(self)
        self._text_group = displayio.Group()
        #self._icon_group = displayio.Group()
        #self._scrolling_group = displayio.Group()
        
        self.append(self._text_group) 
        self.temperature = Label(FONT, color=0x00DD00)
        self.temperature.x = 20
        self.temperature.y = 7
        self._text_group.append(self.temperature)
        #self.append(self._scrolling_group)
        #self.append(self._icon_group)
        # 
        # 
        #         