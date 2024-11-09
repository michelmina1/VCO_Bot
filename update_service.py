import pyodbc,json
import Interfaces.Win32Interface as Win32Interface
import Interfaces.SQLInterface as SQLInterface
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
        self.windowname = Win32Interface.get_window_name(hwnd)
        self.threadid, self.processid = Win32Interface.GetWindowThreadProcessId(hwnd)
        self.process = Win32Interface.get_process_by_id(self.processid)
        self.charname = Win32Interface.read_memory_charname(self)

        self.totalload = Win32Interface.read_memory_totalload(self)
        self.currentload = Win32Interface.read_memory_currentload(self)
        self.wepdura = Win32Interface.read_memory_currentdura(self)
        
        SQLInterface.upsert_account(self)
        self.print_account()
    def print_account(self):
        print(f"Account: {self.charname}")
        print(f"Total Load: {self.totalload}")
        print(f"Current Load: {self.currentload}")
        print(f"Current Durability: {self.wepdura}")
        print()

accounts = [Account(hwnd) for hwnd in Win32Interface.get_all_hwnd()]
