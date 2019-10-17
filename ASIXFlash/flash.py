import usb.util
from usb.util import CTRL_IN, CTRL_OUT, CTRL_TYPE_VENDOR, CTRL_RECIPIENT_DEVICE

# Please change the below MAC address to your preferred value
# There are no checks, so please make sure it is 100% accurate
NEW_MAC_ADDRESS = "1BADCAFEBABE"

BACKUP_EEPROM_FILENAME = "ax88179.bin"

ASIX_VID = 0x0B95
AX_PID = 0x1790

AX_ACCESS_MAC = 0x01
AX_NODE_ID = 0x10
AX_ACCESS_EEPROM = 0x04
AX_RELOAD_EEPROM_EFUSE = 0x06
AX_WRITE_EEPROM_EN = 0x07
AX_WRITE_EEPROM_DIS = 0x08
AX_ETH_ALEN = 6

AX_EEPROM_SIZE_WORDS = 0x43
AX_EEPROM_SIZE_BYTES = 0x86


def write_file(input_bytes: bytearray, filename):
    with open(filename, "wb") as binary_file:
        binary_file.write(input_bytes)
        binary_file.close()

def bytes_to_hex(input_bytes):
    return "".join("{:02X}".format(b) for b in input_bytes)

def control_read(in_dev, request, value, index, length):
    return in_dev.ctrl_transfer(CTRL_IN | CTRL_TYPE_VENDOR | CTRL_RECIPIENT_DEVICE, request, value, index, length)

def control_write(in_dev, request, value, index, data):
    length_written = in_dev.ctrl_transfer(CTRL_OUT | CTRL_TYPE_VENDOR | CTRL_RECIPIENT_DEVICE, request, value, index, data)
    if data is not None:
        if length_written != len(data):
            raise ValueError('Written length does not match requested payload')

def ax_read_node_id_check(in_dev):
    return control_read(in_dev, AX_ACCESS_MAC, AX_NODE_ID, AX_ETH_ALEN, AX_ETH_ALEN)

def ax_get_eeprom_kernel(in_dev):
    read_bytes = bytearray()
    for i in range(AX_EEPROM_SIZE_WORDS):
        single_read_response = control_read(in_dev, AX_ACCESS_EEPROM, i, 1, 2)
        read_bytes.append(single_read_response[0])
        read_bytes.append(single_read_response[1])
    return read_bytes

def ax_set_eeprom_kernel(in_dev, in_bytes):
    if len(in_bytes) % 2 != 0:
        raise ValueError("EEPROM bytes size must be a multiple of 2")
    if len(in_bytes) != 6:
        raise ValueError("MAC address should have exactly 6 octets")

    control_write(in_dev, AX_WRITE_EEPROM_EN, 0, 0, None)
    for i in range(len(in_bytes)):
        if i % 2 != 0:
            continue
        else:
            control_write(in_dev, AX_ACCESS_EEPROM, int(i / 2), 1, bytes([in_bytes[i], in_bytes[i+1]]))
    control_write(in_dev, AX_WRITE_EEPROM_DIS, 0, 0, None)
    control_write(in_dev, AX_RELOAD_EEPROM_EFUSE, 0, 0, None)

if __name__ == "__main__":
    print("Looking for AX88179")
    dev = usb.core.find(idVendor=ASIX_VID, idProduct=AX_PID)
    if dev is None:
        raise ValueError('Device not found. On Windows, remember to change the driver to libusb on Zadig')
    print("Found a matching AX88179 device")
    print("MAC:", bytes_to_hex(ax_read_node_id_check(dev)))
    write_file(ax_get_eeprom_kernel(dev), BACKUP_EEPROM_FILENAME)

    print("Flashing MAC address")
    ax_set_eeprom_kernel(dev, bytes.fromhex(NEW_MAC_ADDRESS))

    print("Flashing complete. \n\nNew device data:")
    print("MAC:", bytes_to_hex(ax_read_node_id_check(dev)))

    print("Completed. Your original EEPROM is saved as", BACKUP_EEPROM_FILENAME)