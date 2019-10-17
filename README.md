# ASIXFlash
_AX88179 Flash Utility for changing the onboard EEPROM's MAC address. 
The changes are persistent, even when plugged into a different device_

![Changed MAC](https://raw.github.com/jglim/ASIXFlash/master/etc/mac-change.png)

Requires **Python 3.6+**, **pyusb** package, and any of these: **libusb 0.1** / **libusb 1.0** / **OpenUSB** 

## How?
- Download and unarchive the repository into a folder
- Open `flash.py`, change the value in `NEW_MAC_ADDRESS = "1BADCAFEBABE"` to a MAC address of your choice.
- Run `pip install pyusb`
- Run `python flash.py`. _This will flash your device with the new MAC address._
- At this point, your device should have been flashed successfully. The original EEPROM will be saved as `ax88179.bin` 

![Demo](https://raw.github.com/jglim/ASIXFlash/master/etc/cmd.png)

## Requirements
- Install LibUSB. 
    - On Windows, there isn't a clear installation process, though [this installer for libusb-0.1 should work](https://sourceforge.net/projects/libusb-win32/files/libusb-win32-releases/1.2.6.0/libusb-win32-devel-filter-1.2.6.0.exe/download)
    - MacOS: via MacPorts, `sudo port install libusb`
    - Linux: `sudo apt-get install libusb-1.0-0-dev`
- Python 3.6+, with `pyusb` 
- (Windows only) Change the loaded AX88179 driver to libusb
    - Run Zadig `zadig-2.4.exe`
    - Select Options -> List all devices (✓)
    - In the dropdown list, select your AX88179 device
    - Press the little arrow on the up-down control until you get an option with `libusb-win32`
    - Click the big button, usually `Replace Driver`

![Zadig Guide](https://raw.github.com/jglim/ASIXFlash/master/etc/zadig.gif)

## License

MIT