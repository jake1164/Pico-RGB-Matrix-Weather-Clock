import board
import digitalio
import storage
'''
To enable persistant storage you need to rename this file to boot.py and place it on your system.
Once renamed and placed on your system you will get a ReadOnly error when you try to copy files to the 
device. You must hold the Menu button (KEY0) while turning on the device to make the device writable
by your computer / usb device. 
'''
write_pin = digitalio.DigitalInOut(board.GP15)
write_pin.direction = digitalio.Direction.INPUT
write_pin.pull = digitalio.Pull.UP

# The filesystem is writable by CircuitPython by default. To modify the
# files via the file system you need to hold the menu (KEY0) button. 
if write_pin.value:
    storage.remount("/", readonly=False)
else:    
    storage.remount("/", readonly=True)