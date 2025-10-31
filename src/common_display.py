import terminalio
import displayio

from adafruit_display_text.scrolling_label import ScrollingLabel
from adafruit_display_text import label

class CommonDisplay(displayio.Group):
    def __init__(self, icon_file, message) -> None:
        super().__init__()
        ICON_X = 1
        ICON_Y = 1
        DISPLAY_WIDTH = 64
        DISPLAY_HEIGHT = 32
        
        try:
            icon = displayio.OnDiskBitmap(icon_file)
            image_width = icon.width
            image_height = icon.height

            bg = displayio.TileGrid(
                icon,
                pixel_shader=getattr(icon, 'pixel_shader', displayio.ColorConverter()),
                width=1,
                height=1,
                tile_width=image_width,
                tile_height=image_height,
                x=ICON_X,
                y=ICON_Y
            )
            self.append(bg)
        except Exception as e:
            print('Error loading icon:', e)

        # Use a non-scrolling label for short text, scrolling for longer
        if len(message) < 20:
            self._scroll_label = False
            self.message_label = label.Label(
                terminalio.FONT,
                text=message,
                color=0xFFFF00,  # Yellow
            )
        else:
            self._scroll_label = True
            self.message_label = ScrollingLabel(
                terminalio.FONT, 
                color=0xFFFF00,  # Yellow color
                text=message,
                max_characters=len(message),
                animate_time=0.8
            )

        self.message_label.anchor_point = (1.0, 1.0)
        self.message_label.anchored_position = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.append(self.message_label)

    def scroll(self) -> None:
        if getattr(self, '_scroll_label', False):
            self.message_label.update()
