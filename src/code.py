# UPDATE the settings.toml file before starting!

# Following are imported from circuitpython 8.x
import os
import gc
import board
import displayio
import framebufferio
from rgbmatrix import RGBMatrix 

# Imported from lib
import circuitpython_schedule as schedule

# project classes 
from displaySubsystem import DisplaySubsystem
from date_utils import DateTimeProcessing
from key_processing import KeyProcessing
from light_sensor import LightSensor
from network import WifiNetwork
from weather.weather_factory import Factory
from weather.weather_display import WeatherDisplay
from settings import Settings
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

datetime = DateTimeProcessing(settings, network)
showSystem = DisplaySubsystem(display, datetime)
light_sensor = LightSensor(settings, display)
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

# Update the RTC every 60 min (settable via settings.toml file
schedule.every(datetime.get_interval()).minutes.do(datetime.update_from_ntp)

#update weather every min
if weather is not None:
    schedule.every(weather.get_update_interval()).seconds.do(weather.show_weather)

weather.show_weather()

print('free memory', gc.mem_free())
while True:
    light_sensor.check_light_sensor()
    if light_sensor.is_dimming():
        continue

    key_value = key_input.get_key_value()    
    key_input.key_processing(key_value)
    
    if key_value is None and key_input.page_id == 0:
        weather.show_datetime()
        if not buzzer.is_beeping(): #This is a hack to try to stop buzzer from buzzing while doing something that might hang.            
            schedule.run_pending()
            weather.scroll_label(key_input) 
    if key_input.page_id == 1:
        showSystem.showSetListPage(key_input.select_setting_options)        
    if key_input.page_id == 2 and key_input.select_setting_options == 0:
        showSystem.timeSettingPage(key_input.time_setting_label)
    if key_input.page_id == 2 and key_input.select_setting_options == 1:
        showSystem.dateSettingPage(key_input.time_setting_label)
    if key_input.page_id == 2 and key_input.select_setting_options > 1:
        showSystem.onOffPage(
            key_input.select_setting_options, 
            settings
        )
