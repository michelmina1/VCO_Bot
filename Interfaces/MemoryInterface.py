import win32gui, win32process, struct,psutil
from math import trunc
from ReadWriteMemory import ReadWriteMemory

def get_all_hwnd() -> list:
    def callback(hwnd, hwnds):
        windowname=win32gui.GetWindowText(hwnd)
        process_id = GetWindowThreadProcessId(hwnd)[1]
        execname = psutil.Process(process_id).name()
        if execname == "Core.exe" and ' ' not in windowname:
            hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds
def read_memory_currentload(account):
    base_address = 0x10000000
    static_address_offset = 0x0007E320
    pointer_static_address = base_address + static_address_offset
    offsets = [0x8, 0x74, 0x4a8, 0x10, 0x28, 0x8, 0x7a4]
    account.process.open()
    my_pointer = account.process.get_pointer(pointer_static_address, offsets=offsets)
    pointer_value = account.process.read(my_pointer)
    
    return trunc(struct.unpack('>f',pointer_value.to_bytes(4, byteorder='big'))[0])
def read_memory_charname(account):
    #TODO: Implement a more robust method to read the charname with length < 16
    base_address = 0x3620000
    static_address_offset = 0x0016D27C
    pointer_static_address = base_address + static_address_offset
    offsets = [0x14, 0xD8, 0x0]
    account.process.open()
    my_pointer = account.process.get_pointer(pointer_static_address, offsets=offsets)
    charname_bytes = b''.join((account.process.read(my_pointer + i) & 0xFF).to_bytes(1, byteorder='big') for i in range(16))  # Read 16 bytes for the charname
    charname = charname_bytes.decode('utf-8', errors='ignore').rstrip('\x00')  # Decode and strip null bytes
    charname = ''.join(filter(lambda x: x.isprintable(), charname))  # Remove non-printable characters
    return charname
def read_memory_totalload(account):
    base_address = 0x10000000
    static_address_offset = 0x000792B4
    pointer_static_address = base_address + static_address_offset
    offsets = [0x10, 0x10, 0x68, 0x200, 0x174, 0x8, 0x7cc]
    account.process.open()
    my_pointer = account.process.get_pointer(pointer_static_address, offsets=offsets)
    pointer_value = account.process.read(my_pointer)
    
    return trunc(struct.unpack('>f',pointer_value.to_bytes(4, byteorder='big'))[0])

def read_memory_locx(account):
    base_address = 0x3210000
    static_address_offset = 0x000942dc
    pointer_static_address = base_address + static_address_offset
    account.process.open()
    #using static memory address not a pointer
    my_pointer = account.process.get_pointer(pointer_static_address)
    pointer_value = account.process.read(my_pointer)
    return trunc(struct.unpack('>f',pointer_value.to_bytes(4, byteorder='big'))[0])

def read_memory_locy(account):
    base_address = 0x3210000
    static_address_offset = 0x000942d8
    pointer_static_address = base_address + static_address_offset
    offsets = [0x0]
    account.process.open()
    #using static memory address not a pointer
    my_pointer = account.process.get_pointer(pointer_static_address)
    pointer_value = account.process.read(my_pointer)
    
    return trunc(struct.unpack('>f',pointer_value.to_bytes(4, byteorder='big'))[0])
def read_memory_currentdura(account):
    base_address = 0x10000000
    static_address_offset = 0x000792B4
    pointer_static_address = base_address + static_address_offset
    offsets = [0x10, 0x10, 0x68, 0x21C, 0x4E8, 0xC, 0xEC]
    account.process.open()
    my_pointer = account.process.get_pointer(pointer_static_address, offsets=offsets)
    pointer_value = account.process.read(my_pointer)
    return pointer_value
def get_window_name(hwnd):
    return win32gui.GetWindowText(hwnd)
def GetWindowThreadProcessId(hwnd):
    return win32process.GetWindowThreadProcessId(hwnd)
def get_process_by_id(process_id):
    return ReadWriteMemory().get_process_by_id(process_id)
