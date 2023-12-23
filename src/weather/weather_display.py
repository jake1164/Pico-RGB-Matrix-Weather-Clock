import time
import gc
import os
import displayio
from collections import deque
#from adafruit_display_text.label import Label
from adafruit_display_text import bitmap_label
from adafruit_bitmap_font import bitmap_font

COLOR_SCROLL = 0x0000DD  # Dark blue
COLOR_TEMP = 0x00DD00    # Green
COLOR_TIME = 0x00DDDD    # Light Blue
COLOR_DARK = 0x800000    # Dark Red
SCROLL_DELAY = 0.06       # How fast does text scroll
SCROLL_END_WAIT = 0.75    # How long do you display the label after the scrolling ends.

class WeatherDisplay(displayio.Group):
    def __init__(self, display, icons) -> None:
        super().__init__()
        self._display = display
        small_font = "/fonts/helvB12.bdf"
        glyphs = b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,.: "
        self._pallete = displayio.Palette(2)
        self._pallete[0] = 0x000000
        self._pallete[1] = COLOR_DARK

        self._random_pixel = displayio.Bitmap(64, 32, 2)

        self.units = os.getenv('UNITS')
        
        self._small_font = bitmap_font.load_font(small_font)
        self._small_font.load_glyphs(glyphs)
        self._small_font.load_glyphs(("°",))

        self._dark_mode = False

        icon_width = 16
        icon_height = 16

        self._current_icon = None
        
        self.scroll_queue = deque((), 5) # TODO: this size needs to come from openweather.. 

        self.root_group = displayio.Group()      
        self._text_group = displayio.Group()
        self._icon_group = displayio.Group()
        self._scrolling_group = displayio.Group()        
        self._random_pixel_group = displayio.Group()
        self._random_pixel_group.append(displayio.TileGrid(self._random_pixel, pixel_shader=self._pallete))

        self._scrolling_group.y = 25
        # _scrolling_group.x is set during scrolling

        self._icon_group.x = 48
        self._icon_group.y = 0

        self.temperature = bitmap_label.Label(self._small_font, color=COLOR_TEMP)        
        self.temperature.x = 1
        self.temperature.y = 5

        self.time = bitmap_label.Label(self._small_font, color=COLOR_TIME)
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
                self._icon_sprite.hidden = True
            else:
                self.temperature.color = COLOR_TEMP
                self.time.color = COLOR_TIME
                self._icon_sprite.hidden = False


    def set_temperature(self, temp):        
        self.temperature.text = self.get_temperature(temp)


    def get_temperature(self, temp):        
        if self.units == 'metric':
            unit = "%d°C"
        else:
            unit = "%d°F"                  
        return unit % temp


    def hide_temperature(self):
        self.temperature.text = ""
        if self._icon_group:
            self._icon_group.pop()        


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


    def set_time(self, time_string) -> bool:
        if self.time.text != time_string:
            self.time.text = time_string
            return True
        return False

    
    def set_humidity(self, humidity):
        self.scroll_queue.append(f'{humidity}% humidity')        


    def set_description(self, description_text):
        self.scroll_queue.append(description_text)


    def set_feels_like(self, feels_like):
        self.scroll_queue.append("Feels Like " + self.get_temperature(feels_like))


    def set_date(self, date_text):        
        self.scroll_queue.append(date_text)       


    def set_wind(self, wind):       
        if self.units == "imperial":
            self.scroll_queue.append(f'wind {wind:.1f} mph')
        else:
            self.scroll_queue.append(f'wind {wind:.1f} m/s')


    def add_text_display(self, text):
        self.scroll_queue.append(text)


    def scroll_label(self, key_input):
        '''
        Scrolls the label until all the text has been shown
        TODO: Includes a hack to check if a button has been pressed to exit early because user is trying to get into the settings menu.
        '''      
        # Button press leaves items in scroll group and mucks things up
        while len(self._scrolling_group) > 0:
            self._scrolling_group.pop()

        if self.scroll_queue:
            scroll_text = self.scroll_queue.popleft()
            scroll_label = bitmap_label.Label(self._small_font, color=COLOR_DARK if self._dark_mode else COLOR_SCROLL , text=scroll_text)            
            text_length = scroll_label.bounding_box[2]

            self._scrolling_group.x = self._display.width
            self._scrolling_group.append(scroll_label)            

            # Start scrolling label
            for _ in range(text_length + 1):
                self._scrolling_group.x = self._scrolling_group.x - 1
                if key_input.get_key_value() is not None:
                    return
                time.sleep(SCROLL_DELAY)
            time.sleep(SCROLL_END_WAIT)
            self._scrolling_group.pop()
            del scroll_label
            gc.collect()
            

    def show(self):
        self._display.root_group = self.root_group


    def hide_pixel(self, x, y):
        self._random_pixel[x, y] = 0

    
    def show_pixel(self, x, y):
        print('show pixel', x, y)
        #TODO: only run this once.
        self._display.root_group = self._random_pixel_group
        #TODO: This is what is changed:
        self._random_pixel[x, y] = 1
    

    @property
    def brightness(self):
        return self._display.brightness
    

    @brightness.setter
    def brightness(self, val):
        self._display.brightness = val