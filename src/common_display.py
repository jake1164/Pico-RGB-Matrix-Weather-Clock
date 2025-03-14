import terminalio
import displayio

from adafruit_display_text.scrolling_label import ScrollingLabel

class CommonDisplay(displayio.Group):
    def __init__(self, icon_file, message) -> None:
        super().__init__()
        ICON_X = 1
        ICON_Y = 1
        DISPLAY_WIDTH = 64
        DISPLAY_HEIGHT = 32
        
        try:
            icon = displayio.OnDiskBitmap(icon_file)
            icon_width = icon.width
            icon_height = icon.height

            bg = displayio.TileGrid(
                icon,
                pixel_shader=getattr(icon, 'pixel_shader', displayio.ColorConverter()),
                width=1,
                height=1,
                tile_width=icon_width,
                tile_height=icon_height,
                x=ICON_X,
                y=ICON_Y
            )
            self.append(bg)
        except Exception as e:
            print('Unable to load icon', e)

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
        self.message_label.update()