# This example implements a simple two line scroller using
# Adafruit_CircuitPython_Display_Text. Each line has its own color
# and it is possible to modify the example to use other fonts and non-standard
# characters.

## To ignore the code.py overriding the std lib error add the following
## to your .vscode.json config file.
##  "python.languageServer": "Pylance",
##  [...]
##  "python.analysis.diagnosticSeverityOverrides": {
##      "reportShadowedImports": "none"
##  },

import time
import adafruit_display_text.label
import board
import displayio
import framebufferio

#import terminalio
import circuitpython_schedule as schedule
from displaySubsystem import DisplaySubsystem

from date_utils import DateTimeProcessing
from key_processing import KeyProcessing
from light_sensor import LightSensor
from rgbmatrix import RGBMatrix # rgbmatrix is included in circuitpython 8.x

## Pins defined here will make it more obvious whats going on?

bit_depth_value = 1
base_width = 64
base_height = 32
chain_across = 1
tile_down = 1
serpentine_value = True

width_value = base_width * chain_across
height_value = base_height * tile_down

# If there was a display before (protomatter, LCD, or E-paper), release it so
# we can create ours
displayio.release_displays()

# This next call creates the RGB Matrix object itself. It has the given width
# and height. bit_depth can range from 1 to 6; higher numbers allow more color
# shades to be displayed, but increase memory usage and slow down your Python
# code. If you just want to show primary colors plus black and white, use 1.
# Otherwise, try 3, 4 and 5 to see which effect you like best.
#
# These lines are for the Feather M4 Express. If you're using a different board,
# check the guide to find the pins and wiring diagrams for your board.
# If you have a matrix with a different width or height, change that too.
# If you have a 16x32 display, try with just a single line of text.

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
#display.rotation = 0


#line1 = adafruit_display_text.label.Label(terminalio.FONT, color=0x00DD00)
#line2 = adafruit_display_text.label.Label(terminalio.FONT, color=0x00DDDD)
#line3 = adafruit_display_text.label.Label(terminalio.FONT, color=0x0000DD)

#line3.x = 12
#line3.y = 56

# Put each line of text into a Group, then show that group.
#g = displayio.Group()
#g.append(line1)
#g.append(line2)
#g.append(line3)
#display.show(g)

time_format_flag = 0 # 12 or 24 (0 or 1) hour display.
datetime = DateTimeProcessing(time_format_flag)
showSystem = DisplaySubsystem(display, datetime)
light_sensor = LightSensor(display)
key_input = KeyProcessing(light_sensor, datetime)

#Update the clock when first starting.
# TODO: Make async
datetime.update_from_ntp()
# Update the RTC every 60 min (settable via settings.toml file
schedule.every(datetime.get_interval()).minutes.do(datetime.update_from_ntp)

while True:
    schedule.run_pending()    
    light_sensor.check_light_sensor()
    key_value = key_input.get_key_value()
    # TODO: key processing should return the page being displayed
    key_input.key_processing(key_value)

    if key_input.page_id == 0:
        #showSystem.showDateTimePage(line1, line2, line3)
        showSystem.showDateTimePage()
    if key_input.page_id == 1:
        #line3.text = ""
        #showSystem.showSetListPage(line1, line2, key_input.select_setting_options)
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
