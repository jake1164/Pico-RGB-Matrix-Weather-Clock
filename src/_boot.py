import board
import digitalio
import storage

write_pin = digitalio.DigitalInOut(board.GP15)
write_pin.direction = digitalio.Direction.INPUT
write_pin.pull = digitalio.Pull.UP

# The filesystem is writable by CircuitPython by default. To modify the
# files via the file system you need to hold the menu (KEY0) button. 
if write_pin.value:
    storage.remount("/", readonly=False)
else:    
    storage.remount("/", readonly=True)