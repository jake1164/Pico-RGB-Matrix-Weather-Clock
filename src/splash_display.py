import terminalio
import displayio

from adafruit_display_text import bitmap_label

class SplashDisplay(displayio.Group):
    def __init__(self, icons, version) -> None:
        super().__init__()
        ICON_X = 24
        ICON_Y = 1       
        VERSION_X = 1
        VERSION_Y = 28

        bg = displayio.TileGrid(
            icons,
            pixel_shader=getattr(icons, 'pixel_shader', displayio.ColorConverter()),
            tile_width=16,
            tile_height=16,
            x=ICON_X,
            y=ICON_Y
        )
        version_label = bitmap_label.Label(terminalio.FONT, color=0x00DD00)
        version_label.text = f'{version.get_version_string()}'
        version_label.x = VERSION_X
        version_label.y = VERSION_Y
        self.append(bg)
        self.append(version_label)
