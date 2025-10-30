# UPDATE the settings.toml file before starting!

# Following are imported from circuitpython 9.x
import os
import gc
import board
import displayio
import time
import microcontroller
import framebufferio
from rgbmatrix import RGBMatrix

RGB_PINS = [board.GP2, board.GP3, board.GP4, board.GP5, board.GP8, board.GP9]
ADDR_PINS = [board.GP10, board.GP16, board.GP18, board.GP20]
CLOCK_PIN = board.GP11
LATCH_PIN = board.GP12
OUTPUT_ENABLE_PIN = board.GP13

gc.collect()
icon_spritesheet_file = "/images/weather-icons.bmp"
splash_img_file = "/images/ow.bmp"
time_format_flag = 0 # 12 or 24 (0 or 1) hour display.

BASE_WIDTH = 64
BASE_HEIGHT = 32

## Set this to be either 32 or 64 based on the size matrix you have.
BIT_DEPTH_VALUE = 1
CHAIN_ACROSS = 1
TILE_DOWN = 1
SERPENTINE_VALUE = True

# Weather update timeout (seconds) before watchdog reset. Configurable via settings.toml (WEATHER_TIMEOUT)
_weather_timeout_env = os.getenv('WEATHER_TIMEOUT')
try:
    WEATHER_TIMEOUT = int(_weather_timeout_env) if _weather_timeout_env is not None else 300
    # Basic sanity: enforce reasonable lower bound
    if WEATHER_TIMEOUT < 30:
        WEATHER_TIMEOUT = 30
except Exception:
    WEATHER_TIMEOUT = 300
del _weather_timeout_env

from version import Version
version = Version()
# read the version if it exists.
print(f'Version: {version.get_version_string()}')

# release displays  before creating a new one.
displayio.release_displays()

calcuated_width = BASE_WIDTH * CHAIN_ACROSS
calculated_height = BASE_HEIGHT * TILE_DOWN

# This next call creates the RGB Matrix object itself. It has the given width
# and height. bit_depth can range from 1 to 6; higher numbers allow more color
# shades to be displayed, but increase memory usage and slow down your Python
# code. If you just want to show primary colors plus black and white, use 1.
# Otherwise, try 3, 4 and 5 to see which effect you like best.

matrix = RGBMatrix(
    width = calcuated_width,
    height=calculated_height,
    bit_depth=BIT_DEPTH_VALUE,
    rgb_pins=RGB_PINS,
    addr_pins=ADDR_PINS,
    clock_pin=CLOCK_PIN,
    latch_pin=LATCH_PIN,
    output_enable_pin=OUTPUT_ENABLE_PIN,
    tile=TILE_DOWN,
    serpentine=SERPENTINE_VALUE,
    doublebuffer=True,
)
del calcuated_width, calculated_height

# Associate the RGB matrix with a Display so that we can use displayio features
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True)

#display a splash screen to hide the random text that appears.
from common_display import CommonDisplay
splash = CommonDisplay(splash_img_file, version.get_version_string())
display.root_group = splash
splash.scroll()

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

try:
    # check that the settings.toml file exists.
    try:
        os.stat('settings.toml')
    except OSError:
        raise Exception('settings.toml file not found.. rename settings.toml.default to settings.toml')

    network = WifiNetwork()
except Exception as e:
    print('Network exception: ', e)
    try:
        error_display = CommonDisplay("/images/wifi.bmp", str(e))
        display.root_group = error_display
        while True:
            error_display.scroll()
        # loops above and does not continue.
    except Exception as ex:
        print(ex)
    # if error display errored out then exit.
    import sys
    sys.exit()

icons = displayio.OnDiskBitmap(icon_spritesheet_file)

settings = Settings()
buzzer = Buzzer(settings)
light_sensor = LightSensor(settings)

datetime = DateTimeProcessing(settings, network)
key_input = KeyProcessing(settings, datetime, buzzer)

weather_display = WeatherDisplay(display, icons)

try:
    weather = OpenWeather(weather_display, network, datetime)
except Exception as e:
    print("Unable to configure weather, exiting")
    try:
        error_display = CommonDisplay("/images/config_error.bmp", str(e))
        display.root_group = error_display
        while True:
            error_display.scroll()
        # loops above and does not continue.
    except Exception as ex:
        print(ex)
    # if error display errored out then exit.
    import sys
    sys.exit()


#Update the clock when first starting.
# TODO: Make async
datetime.update_from_ntp()
last_ntp = time.monotonic()

# Get the initial display and set it.
try:
    weather.show_weather()
except Exception as e:
    print('Initial weather display failed:', e)
last_weather = time.monotonic()
settings_visited = False

# remove splash from memory
#del bg, splash
del splash
gc.collect()

print('free memory after loading', gc.mem_free())
while True:
    # Always process keys first
    key_value = key_input.get_key_value()
    key_input.key_processing(key_value)

    if key_value is None and key_input.page_id == 0: # normal display
        if settings_visited:
            settings_visited = False
            del settings_display
            while len(weather_display.scroll_queue) > 0:
                weather_display.scroll_queue.popleft()
            weather.show_weather()
            gc.collect()
            
        # current_time in seconds > start_time in seconds + interval in seconds.
        if time.monotonic() - last_ntp > datetime.get_interval():
            datetime.update_from_ntp()
            last_ntp = time.monotonic()
        if weather.show_datetime(): # returns true if autodim enabled and outside of time
            darkmode = light_sensor.get_display_mode()
            weather_display.set_display_mode(darkmode)
            #This is a hack to try to stop buzzer from buzzing while doing something that might hang.
            if not buzzer.is_beeping():
                if weather.weather_complete() and (time.monotonic() - last_weather > weather.get_update_interval()):
                    try:
                        try:
                            weather.show_weather()
                            last_weather = time.monotonic()
                        except Exception as e:
                            print('Initial weather update failed:', e)
                            last_weather = None
                    except Exception as e:
                        print('Weather update failed:', e)
                weather_display.scroll_label(key_input)
            if last_weather is not None and (time.monotonic() - last_weather > WEATHER_TIMEOUT):
                print('No weather update for', WEATHER_TIMEOUT, 'seconds during active period. Restarting controller...')
                microcontroller.reset()

    elif key_input.page_id == 1: # Process settings pages
        if not settings_visited:
            weather.display_off()
            settings_visited = True
        settings_display = SettingsDisplay(display, datetime)
        settings_display.showSetListPage(key_input.select_setting_options)
        
    elif key_input.page_id == 2: # Process settings pages
        if SETTINGS[key_input.select_setting_options]["type"] == 'set_time':
            settings_display.timeSettingPage(key_input.select_setting_options, key_input.time_setting_label)
        elif SETTINGS[key_input.select_setting_options]["type"] == 'set_date':
            settings_display.dateSettingPage(key_input.select_setting_options, key_input.time_setting_label)
        elif SETTINGS[key_input.select_setting_options]["type"] == 'bool':
            settings_display.onOffPage(
                key_input.select_setting_options, 
                settings
            )
        elif SETTINGS[key_input.select_setting_options]["type"] == 'number':
            settings_display.number_display_page(key_input.select_setting_options, settings)
        elif SETTINGS[key_input.select_setting_options]["type"] == 'time':
            settings_display.time_page(
                key_input.select_setting_options,
                SETTINGS[key_input.select_setting_options]["text"],
                settings.on_time if key_input.select_setting_options == 8 else settings.off_time
            )