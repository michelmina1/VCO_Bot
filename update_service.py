import pyodbc,json
import Interfaces.MemoryInterface as MemoryInterface
import Interfaces.SQLInterface as SQLInterface
import time
def init_db():
    with open('botconfig.json', 'r') as file:
        config = json.load(file)
    
    connection_string = config['database']['connection_string']
    if 'username' in config['database'] and 'password' in config['database']:
        connection_string += f" UID={config['database']['username']}; PWD={config['database']['password']};"
    if config['database'].get('trust_server', False):
        connection_string += " TrustServerCertificate=yes;"
    
    # Connect to the database
    conn = pyodbc.connect(connection_string)
    return conn

class Account:
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.windowname = MemoryInterface.get_window_name(hwnd)
        self.threadid, self.processid = MemoryInterface.GetWindowThreadProcessId(hwnd)
        self.process = MemoryInterface.get_process_by_id(self.processid)
        self.charname = self.windowname
        #self.charname = Win32Interface.read_memory_charname(self)

        self.totalload = MemoryInterface.read_memory_totalload(self)
        self.currentload = MemoryInterface.read_memory_currentload(self)
        self.wepdura = MemoryInterface.read_memory_currentdura(self)
        self.x = MemoryInterface.read_memory_locx(self)
        self.y = MemoryInterface.read_memory_locy(self)
        
        SQLInterface.upsert_account(self)
        #self.print_account()
    def print_account(self):
        print(f"Account: {self.charname}")
        print(f"Total Load: {self.totalload}")
        print(f"Current Load: {self.currentload}")
        print(f"Current Durability: {self.wepdura}")
        print(f"X: {self.x}")
        print(f"Y: {self.y}")
        print()

accounts = [Account(hwnd) for hwnd in MemoryInterface.get_all_hwnd()]

while(True):
    for account in accounts:
        account.__init__(account.hwnd)
    time.sleep(0.1)