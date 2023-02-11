import os
import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font

cwd = ("/" + __file__).rsplit("/", 1)[
    0
]

class BaseDisplay(displayio.Group):
    def __init__(self) -> None:
        super().__init__()
        icon_spritesheet = "/images/weather-icons.bmp"
        small_font = "/fonts/Arial-12.bdf"        
        glyphs = b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,.: "

        self._units = os.getenv('UNITS')
        
        self._small_font = bitmap_font.load_font(small_font)
        self._small_font.load_glyphs(glyphs)
        self._small_font.load_glyphs(("°",))

        icons = displayio.OnDiskBitmap(open(icon_spritesheet, "rb"))
        icon_width = 16
        icon_height = 16
        scrolling_text_height = 24
        scroll_delay = 0.03                
        self._current_icon = None
        self._scroll_text = []

        self.root_group = displayio.Group()        
        self._text_group = displayio.Group()
        self._icon_group = displayio.Group()        
        self._scrolling_group = displayio.Group()
        self.root_group.append(self)

        self.append(self._text_group) 
        self.temperature = Label(self._small_font, color=0x00DD00)
        self.temperature.x = 20
        self.temperature.y = 7
        self._text_group.append(self.temperature)
        
        self.append(self._scrolling_group)
        self.append(self._icon_group)

        self._icon_sprite = displayio.TileGrid(
            icons,
            pixel_shader=getattr(icons, 'pixel_shader', displayio.ColorConverter()),
            tile_width=icon_width,
            tile_height=icon_height
        )

        self.set_icon(None)


    def set_temperature(self, temp):        
        if self._units:
            unit = "%d°F"
        else:
            unit = "%d°C"
        
        self.temperature.text = unit % temp


    def set_icon(self, name):
        if self._current_icon == name:
            return
        self._current_icon = name

        icon_map = ("01", "02", "03", "04", "09", "10", "11", "13", "50")        
        if self._icon_group:
            self._icon_group.pop()
        if name is not None:
            row = None
            for index, icon in enumerate(icon_map):
                if icon == name[0:2]:
                    row = index
                    break
            column = 0
            if name[2] == "n":
                column = 1
            if row is not None:
                self._icon_sprite[0] = (row * 2) + column
                self._icon_group.append(self._icon_sprite)

