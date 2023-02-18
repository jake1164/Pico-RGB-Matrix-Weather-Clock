import time
import os
import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.circle import Circle

class WeatherDisplay(displayio.Group):
    def __init__(self, display) -> None:
        super().__init__()
        self._display = display
        icon_spritesheet = "/images/weather-icons.bmp"
        small_font = "/fonts/helvB12.bdf"
        #small_font = "/fonts/SteelfishRg-Regular-9.bdf"
        glyphs = b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,.: "
        self._current_label = None #index of current label

        self.units = os.getenv('UNITS')
        
        self._small_font = bitmap_font.load_font(small_font)
        self._small_font.load_glyphs(glyphs)
        self._small_font.load_glyphs(("°",))

        icons = displayio.OnDiskBitmap(open(icon_spritesheet, "rb"))
        icon_width = 16
        icon_height = 16
        
        self.scroll_delay = 0.03
        self._current_icon = None
        self._scroll_array = []
        self.scroll_description = Label(self._small_font, color=0x0000DD)
        self.scroll_humidity = Label(self._small_font, color=0x0000DD)
        self.scroll_date = Label(self._small_font, color=0x0000DD)
        self.scroll_feels = Label(self._small_font, color=0x0000DD)
        self._scroll_array.append(self.scroll_description)
        self._scroll_array.append(self.scroll_date)
        self._scroll_array.append(self.scroll_humidity)
        self._scroll_array.append(self.scroll_feels)

        self.root_group = displayio.Group()      
        self._text_group = displayio.Group()
        self._icon_group = displayio.Group()
        self._scrolling_group = displayio.Group()    
        self._wind_icon_group = displayio.Group()

        self._icon_group.x = 48
        self._icon_group.y = 0

        self.temperature = Label(self._small_font, color=0x00DD00)
        self.temperature.x = 1
        self.temperature.y = 5

        self.time = Label(self._small_font, color=0x00DDDD)
        self.time.anchor_point = (0, 0)
        self.time.x = 0
        self.time.y = 15
        #self.circle = Circle(40, 6, 5, outline=0xFF00FF)
        #self._wind_icon_group.append(self.circle)

        self.root_group.append(self)
        self._text_group.append(self.time)
        self._text_group.append(self.temperature)
        self.append(self._text_group) 
        self.append(self._scrolling_group)
        self.append(self._icon_group)
        #self.append(self._wind_icon_group)

        self._icon_sprite = displayio.TileGrid(
            icons,
            pixel_shader=getattr(icons, 'pixel_shader', displayio.ColorConverter()),
            tile_width=icon_width,
            tile_height=icon_height
        )

        self.set_icon(None)


    def set_temperature(self, temp):        
        self.temperature.text = self.get_temperature(temp)


    def get_temperature(self, temp):        
        if self.units:
            unit = "%d°F"
        else:
            unit = "%d°C"
        
        return unit % temp



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


    def set_time(self, time_string):
        self.time.text = time_string

    
    def set_humidity(self, humidity):
        pass

    def set_description(self, description_text):
        self.scroll_description.text = description_text

    def set_feels_like(self, feels_like):
        self.scroll_feels.text = "Feels Like " + self.get_temperature(feels_like)

    def set_date(self, date_text):
        self.scroll_date.text = date_text


    def scroll_label(self):
        if self._current_label is not None and self._scrolling_group:
            current_text = self._scroll_array[self._current_label]
            text_width = current_text.bounding_box[2]
            for _ in range(text_width + 1):
                self._scrolling_group.x = self._scrolling_group.x - 1
                time.sleep(self.scroll_delay)

        if self._current_label is not None:
            self._current_label += 1
        if self._current_label is None or self._current_label >= len(self._scroll_array):
            self._current_label = 0

        
        if self._scrolling_group:
            self._scrolling_group.pop()

        current_text = self._scroll_array[self._current_label]
        self._scrolling_group.append(current_text)

        self._scrolling_group.x = self._display.width
        self._scrolling_group.y = 25

        for _ in range(self._display.width):
            self._scrolling_group.x = self._scrolling_group.x - 1
            time.sleep(self.scroll_delay)

    def show(self):
        self._display.show(self.root_group)