import time
import gc
import os
import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font

COLOR_SCROLL = 0x0000DD  # Dark blue
COLOR_TEMP = 0x00DD00    # Green
COLOR_TIME = 0x00DDDD    # Light Blue
COLOR_DARK = 0x800000    # Dark Red

class WeatherDisplay(displayio.Group):
    def __init__(self, display, icons) -> None:
        super().__init__()
        self._display = display
        small_font = "/fonts/helvB12.bdf"
        glyphs = b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,.: "
        self._current_label = None #index of current label

        self.units = os.getenv('UNITS')
        
        self._small_font = bitmap_font.load_font(small_font)
        self._small_font.load_glyphs(glyphs)
        self._small_font.load_glyphs(("°",))

        self._dark_mode = False

        icon_width = 16
        icon_height = 16

        self.scroll_delay = 0.03
        self._current_icon = None
        self._scroll_array = []
        self.scroll_description = Label(self._small_font, color=COLOR_SCROLL)
        self.scroll_humidity = Label(self._small_font, color=COLOR_SCROLL)
        self.scroll_date = Label(self._small_font, color=COLOR_SCROLL)
        self.scroll_feels = Label(self._small_font, color=COLOR_SCROLL)
        self.scroll_wind = Label(self._small_font, color=COLOR_SCROLL)
        self._scroll_array.append(self.scroll_description)
        self._scroll_array.append(self.scroll_date)
        self._scroll_array.append(self.scroll_humidity)
        self._scroll_array.append(self.scroll_feels)
        self._scroll_array.append(self.scroll_wind)

        self.root_group = displayio.Group()      
        self._text_group = displayio.Group()
        self._icon_group = displayio.Group()
        self._scrolling_group = displayio.Group()        

        self._icon_group.x = 48
        self._icon_group.y = 0

        self.temperature = Label(self._small_font, color=COLOR_TEMP)        
        self.temperature.x = 1
        self.temperature.y = 5

        self.time = Label(self._small_font, color=COLOR_TIME)
        self.time.anchor_point = (0, 0)
        self.time.x = 0
        self.time.y = 15

        self.root_group.append(self)
        self._text_group.append(self.time)
        self._text_group.append(self.temperature)

        self.append(self._text_group) 
        self.append(self._scrolling_group)
        self.append(self._icon_group)

        self._icon_sprite = displayio.TileGrid(
            icons,
            pixel_shader=getattr(icons, 'pixel_shader', displayio.ColorConverter()),
            tile_width=icon_width,
            tile_height=icon_height
        )

        self.set_icon(None)
        gc.collect()


    def set_display_mode(self, darkmode):        
        if self._dark_mode == darkmode:            
            pass # No change
        else:
            self._dark_mode = darkmode # Only change once
            if darkmode:
                self.temperature.color = COLOR_DARK
                self.time.color = COLOR_DARK
                for label in self._scroll_array:
                    label.color = COLOR_DARK
            else:
                self.temperature.color = COLOR_TEMP
                self.time.color = COLOR_TIME
                for label in self._scroll_array:
                    label.color = COLOR_SCROLL


    def set_temperature(self, temp):        
        self.temperature.text = self.get_temperature(temp)


    def get_temperature(self, temp):        
        if self.units == 'metric':
            unit = "%d°C"
        else:
            unit = "%d°F"
            
        
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
        gc.collect()


    def set_time(self, time_string):
        self.time.text = time_string
        print('color changed?', self.time.color)

    
    def set_humidity(self, humidity):
        self.scroll_humidity.text = "%d%% humidity" % humidity


    def set_description(self, description_text):
        self.scroll_description.text = description_text


    def set_feels_like(self, feels_like):
        self.scroll_feels.text = "Feels Like " + self.get_temperature(feels_like)        


    def set_date(self, date_text):
        self.scroll_date.text = date_text


    def set_wind(self, wind):
        if self.units == "imperial":
            self.scroll_wind.text = "wind %d mph" % wind
        else:
            self.scroll_wind.text = "wind %d m/s" % wind


    def scroll_label(self, key_input):
        '''
        Scrolls the label until all the text has been shown
        TODO: Includes a hack to check if a button has been pressed to exit early because user is trying to get into the settings menu.
        '''
        if self._current_label is not None and self._scrolling_group:
            current_text = self._scroll_array[self._current_label]
            text_width = current_text.bounding_box[2]
            for _ in range(text_width + 1):
                self._scrolling_group.x = self._scrolling_group.x - 1
                if key_input.get_key_value() is not None:
                    return
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

            if key_input.get_key_value() is not None:                
                return
            time.sleep(self.scroll_delay)

    def show(self):
        self._display.show(self.root_group)