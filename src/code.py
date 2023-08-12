# UPDATE the settings.toml file before starting!

# Following are imported from circuitpython 8.x
import os
import gc
import board
import displayio
import time
import framebufferio
from rgbmatrix import RGBMatrix 

# project classes 
from settings_display import SETTINGS, SettingsDisplay
from date_utils import DateTimeProcessing
from key_processing import KeyProcessing
from light_sensor import LightSensor
from network import WifiNetwork
from weather.open_weather import OpenWeather
from weather.weather_display import WeatherDisplay
from persistent_settings import Settings
from buzzer import Buzzer

gc.collect()
icon_spritesheet = "/images/weather-icons.bmp"
time_format_flag = 0 # 12 or 24 (0 or 1) hour display.
bit_depth_value = 1
base_width = 64
base_height = 32
chain_across = 1
tile_down = 1
serpentine_value = True

width_value = base_width * chain_across
height_value = base_height * tile_down

# release displays  before creating a new one.
displayio.release_displays()

# This next call creates the RGB Matrix object itself. It has the given width
# and height. bit_depth can range from 1 to 6; higher numbers allow more color
# shades to be displayed, but increase memory usage and slow down your Python
# code. If you just want to show primary colors plus black and white, use 1.
# Otherwise, try 3, 4 and 5 to see which effect you like best.

matrix = RGBMatrix(
    width=width_value,height=height_value,bit_depth=bit_depth_value,
    rgb_pins=[board.GP2, board.GP3, board.GP4, board.GP5, board.GP8, board.GP9],
    addr_pins=[board.GP10, board.GP16, board.GP18, board.GP20],
    clock_pin=board.GP11,latch_pin=board.GP12,output_enable_pin=board.GP13,
    tile=tile_down,serpentine=serpentine_value,
    doublebuffer=True,
)

# Associate the RGB matrix with a Display so that we can use displayio features
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True)

#display a splash screen to hide the random text that appears.
icons = displayio.OnDiskBitmap(open(icon_spritesheet, "rb"))
splash = displayio.Group()
splash.x = 24
splash.y = 8
bg = displayio.TileGrid(
    icons,
    pixel_shader=getattr(icons, 'pixel_shader', displayio.ColorConverter()),
    tile_width=16,
    tile_height=16
)
splash.append(bg)
display.show(splash)

try:
    network = WifiNetwork() # TODO: catch exception and do something meaninful with it.
except Exception as e:
    print('Network exception?', e)

# TODO: Display wifi config icon 

settings = Settings()
buzzer = Buzzer(settings)
light_sensor = LightSensor(settings)

datetime = DateTimeProcessing(settings, network)
#settings_display = SettingsDisplay(display, datetime)
key_input = KeyProcessing(settings, datetime, buzzer)

weather_display = WeatherDisplay(display, icons)

try:
    weather = OpenWeather(weather_display, datetime, network)
except Exception as e:
    print("Unable to configure weather, exiting")
    exit()


#Update the clock when first starting.
# TODO: Make async
datetime.update_from_ntp()
last_ntp = time.time()

# Get the initial display and set it.
weather.show_weather()
last_weather = time.time()
settings_visited = False

print('free memory', gc.mem_free())
while True:
    # Always process keys first
    key_value = key_input.get_key_value()    
    key_input.key_processing(key_value)  
    
    if key_value is None and key_input.page_id == 0: # IF normal display
        if settings_visited:                                    
            settings_visited = False
            del settings_display
            weather_display.scroll_queue.clear()
            gc.collect()
            
        # current_time in seconds > start_time in seconds + interval in seconds.
        if time.time() > last_ntp + datetime.get_interval():            
            datetime.update_from_ntp()
            last_ntp = time.time()
        if weather.show_datetime(): # returns true if autodim enabled and outside of time
            darkmode = light_sensor.get_display_mode()
            weather_display.set_display_mode(darkmode)
            #This is a hack to try to stop buzzer from buzzing while doing something that might hang. 
            if not buzzer.is_beeping():
                if weather.weather_complete() and time.time() > last_weather + weather.get_update_interval():
                    weather.show_weather()
                    last_weather = time.time()               
                weather_display.scroll_label(key_input) 


    elif key_input.page_id == 1: # Process settings pages        
        weather.display_off()
        settings_display = SettingsDisplay(display, datetime)
        settings_display.showSetListPage(key_input.select_setting_options)
        settings_visited = True
    elif key_input.page_id == 2: # Process settings pages
        if SETTINGS[key_input.select_setting_options]["type"] == 'set_time':
            settings_display.timeSettingPage(key_input.time_setting_label)            
        elif SETTINGS[key_input.select_setting_options]["type"] == 'set_date':
            settings_display.dateSettingPage(key_input.time_setting_label)
        elif SETTINGS[key_input.select_setting_options]["type"] == 'bool':
            settings_display.onOffPage(
                key_input.select_setting_options, 
                settings
            )
        elif SETTINGS[key_input.select_setting_options]["type"] == 'number':
            settings_display.number_display_page(settings)
        elif SETTINGS[key_input.select_setting_options]["type"] == 'time':
            settings_display.time_page(
                SETTINGS[key_input.select_setting_options]["text"], 
                settings.on_time if key_input.select_setting_options == 8 else settings.off_time
            )