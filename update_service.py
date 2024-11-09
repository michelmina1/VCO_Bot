import os,datetime
import win32gui, win32process, struct
from math import trunc
from ReadWriteMemory import ReadWriteMemory

def get_all_hwnd() -> list:
    def callback(hwnd, hwnds):
        windowname=win32gui.GetWindowText(hwnd)
        if windowname == "VoyageCentury":
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
def read_memory_totalload(account):
    base_address = 0x10000000
    static_address_offset = 0x000792B4
    pointer_static_address = base_address + static_address_offset
    offsets = [0x10, 0x10, 0x68, 0x200, 0x174, 0x8, 0x7cc]
    account.process.open()
    my_pointer = account.process.get_pointer(pointer_static_address, offsets=offsets)
    pointer_value = account.process.read(my_pointer)
    
    return trunc(struct.unpack('>f',pointer_value.to_bytes(4, byteorder='big'))[0])
def read_memory_slave_type(hwnd2):
    base_address = 0x10000000
    static_address_offset = 0x000792B4
    pointer_static_address = base_address + static_address_offset
    offsets = [0x44c, 0x10, 0x14, 0x1a0, 0x18, 0x11c, 0x1e4, 0x818, 0xc, 0x5ec]
    rwm=ReadWriteMemory()
    mypid = win32process.GetWindowThreadProcessId(hwnd2)[1]
    process = rwm.get_process_by_id(mypid)
    process.open()
    my_pointer = process.get_pointer(pointer_static_address, offsets=offsets)
    pointer_value = process.read(my_pointer)
    return pointer_value
def update_load_data(hwnds):
    for i in range(0,len(hwnds)-1):
        #Updating load data
        currentload[i] = read_memory_currentload(hwnds[i])
        maxload[i] = read_memory_totalload(hwnds[i])
        
        #Updates the hours left according to the slave type
        bot_value=slave_types[i]
        if bot_value == 'FIO':
            hours_left[i] = trunc((maxload[i]-currentload[i])/2.4)
        elif bot_value == 'Coal':
            hours_left[i] = trunc((maxload[i]-currentload[i])/8.5)
        elif bot_value == 'Charcoal':
            hours_left[i] = trunc((maxload[i]-currentload[i])/14.0)
        
        hours_left_lbl[i].configure(text=str(currentload[i])+"/"+str(maxload[i])+"  Hours left = "+str(hours_left[i]))
        
        #Updates the load progressbar and its corresponding color
        progressbar[i].set(currentload[i]/maxload[i])  # --> update progress bars
        pickaxeimages[i].configure(text=str(read_memory_currentdura(hwnds[i]))) 
        if (currentload[i]/maxload[i]*100>75):
            progressbar[i].configure(progress_color='red') # --> updates color of progress bar 
        else:
            progressbar[i].configure(progress_color=["#3a7ebf", "#1f538d"]) # --> updates color of progress bar
def read_memory_currentdura(account):
    base_address = 0x10000000
    static_address_offset = 0x000792B4
    pointer_static_address = base_address + static_address_offset
    offsets = [0x10, 0x10, 0x68, 0x21C, 0x4E8, 0xC, 0xEC]
    account.process.open()
    my_pointer = account.process.get_pointer(pointer_static_address, offsets=offsets)
    pointer_value = account.process.read(my_pointer)
    return pointer_value

class Account:
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.window_text = win32gui.GetWindowText(hwnd)
        self.threadid, self.process_id = win32process.GetWindowThreadProcessId(hwnd)
        self.process = ReadWriteMemory().get_process_by_id(self.process_id)
        self.chartotalload = read_memory_totalload(self)
        self.charload = read_memory_currentload(self)
        self.chardura = read_memory_currentdura(self)
        print(self.window_text, self.chartotalload, self.charload, self.chardura)

accounts = [Account(hwnd) for hwnd in get_all_hwnd()]
