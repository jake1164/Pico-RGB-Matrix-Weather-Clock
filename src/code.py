# UPDATE the settings.toml file before starting!

# Following are imported from circuitpython 8.x
import os
import gc
import board
import displayio
import time
import framebufferio
from rgbmatrix import RGBMatrix 

# Imported from lib
#import circuitpython_schedule as schedule

# project classes 
from displaySubsystem import SETTINGS, DisplaySubsystem
from date_utils import DateTimeProcessing
from key_processing import KeyProcessing
from light_sensor import LightSensor
from network import WifiNetwork
from weather.weather_factory import Factory
from weather.weather_display import WeatherDisplay
from persistent_settings import Settings
from buzzer import Buzzer

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
showSystem = DisplaySubsystem(display, datetime)
key_input = KeyProcessing(settings, datetime, buzzer)

weather_display = WeatherDisplay(display, icons)

try:
    if os.getenv('TEMPEST_ENABLE'):
        weather = Factory('TEMPEST', weather_display, datetime, network)
    elif os.getenv('OWM_ENABLE'):
        weather = Factory('OWM', weather_display, datetime, network)
    else:
        print('Better handling required.')
        raise Exception("No weather api's enabled")
except Exception as e:
    print("Unable to configure weather, exiting")
    exit()


#Update the clock when first starting.
# TODO: Make async
datetime.update_from_ntp()
last_ntp = time.time()
# Update the RTC every 60 min (settable via settings.toml file
#schedule.every(datetime.get_interval()).minutes.do(datetime.update_from_ntp)

#update weather every min
#if weather is not None:
#    schedule.every(weather.get_update_interval()).seconds.do(weather.show_weather)
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
            showSystem.clean()
            settings_visited = False
        # current_time in seconds > start_time in seconds + interval in seconds.
        if time.time() > last_ntp + datetime.get_interval():            
            datetime.update_from_ntp()
            last_ntp = time.time()
        if weather.show_datetime(): # returns true if autodim enabled and outside of time
            darkmode = light_sensor.get_display_mode()
            weather_display.set_display_mode(darkmode)
            #This is a hack to try to stop buzzer from buzzing while doing something that might hang. 
            if not buzzer.is_beeping():
                if time.time() > last_weather + weather.get_update_interval():
                    weather.show_weather()
                    last_weather = time.time()
                #schedule.run_pending()
                #weather.show_weather()                
                weather.scroll_label(key_input) 


    elif key_input.page_id == 1: # Process settings pages        
        weather.display_on()
        showSystem.showSetListPage(key_input.select_setting_options)
        settings_visited = True
    elif key_input.page_id == 2: # Process settings pages
        if SETTINGS[key_input.select_setting_options]["type"] == 'set_time':
            showSystem.timeSettingPage(key_input.time_setting_label)            
        elif SETTINGS[key_input.select_setting_options]["type"] == 'set_date':
            showSystem.dateSettingPage(key_input.time_setting_label)
        elif SETTINGS[key_input.select_setting_options]["type"] == 'bool':
            showSystem.onOffPage(
                key_input.select_setting_options, 
                settings
            )
        elif SETTINGS[key_input.select_setting_options]["type"] == 'number':
            showSystem.number_display_page(settings)
        elif SETTINGS[key_input.select_setting_options]["type"] == 'time':
            showSystem.time_page(
                SETTINGS[key_input.select_setting_options]["text"], 
                settings.on_time if key_input.select_setting_options == 8 else settings.off_time
            )