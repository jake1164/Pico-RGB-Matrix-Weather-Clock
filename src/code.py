# Requires a settings.toml file with the following
# settings in settings file:
# TZ_OFFSET=<timezone offset> ie TZ_OFFSET=-5
# WIFI_SSID="your ssid"
# WIFI_PASSWORD="yoursupersecretpassword"
# NTP_HOST="0.adafruit.pool.ntp.org"
# NTP_INTERVAL=6  

# Following are imported from circuitpython 8.x
import time
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
from weather import open_weather
from weather import tempest_weather

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

network = WifiNetwork() # TODO: catch exception and do something meaninful with it.

datetime = DateTimeProcessing(time_format_flag, network)
showSystem = DisplaySubsystem(display, datetime)
light_sensor = LightSensor(display)
key_input = KeyProcessing(light_sensor, datetime)

weather = None
if os.getenv('TEMPEST_ENABLE'):
    weather = tempest_weather.TempestWeather(display, network)
elif weather is None and os.getenv('OWM_ENABLE'):
    weather = open_weather.OpenWeather(display, network, datetime)


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
    # TODO: key processing should return the page being displayed
    key_input.key_processing(key_value)
    
    if key_input.page_id == 0:
        #showSystem.showDateTimePage()
        schedule.run_pending()
        weather.scroll_label()
        #time.sleep(0)        
    if key_input.page_id == 1:
        showSystem.showSetListPage(key_input.select_setting_options)        
    if key_input.page_id == 2 and key_input.select_setting_options == 0:
        showSystem.timeSettingPage(key_input.time_setting_label)
    if key_input.page_id == 2 and key_input.select_setting_options == 1:
        showSystem.dateSettingPage(key_input.time_setting_label)
    if key_input.page_id == 2 and key_input.select_setting_options > 1:
        showSystem.onOffPage(
            key_input.select_setting_options, 
            key_input._buzzer.enabled, 
            light_sensor.auto_dimming
        )
