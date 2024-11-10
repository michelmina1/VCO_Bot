import pyodbc
import json

# Load database configuration from botconfig.json
with open('botconfig.json', 'r') as config_file:
    config = json.load(config_file)
    connection_string = config['database']['connection_string']
    username = config['database']['username']
    password = config['database']['password']

    def upsert_account(account):
        conn = pyodbc.connect(connection_string, user=username, password=password)
        cursor = conn.cursor()
    
        # Check if the account exists
        cursor.execute("SELECT COUNT(*) FROM Account WHERE name = ?", account.charname)
        exists = cursor.fetchone()[0]
        
        if exists:
            # Update the existing account
            cursor.execute("""
                UPDATE Account
                SET hwnd = ?, threadID = ?, ProcessID = ?, WindowName = ?
                WHERE name = ?
            """, account.hwnd, account.threadid, account.processid, account.windowname, account.charname)
            conn.commit()
            # Get the account ID
            cursor.execute("SELECT accountid FROM Account WHERE name = ?", account.charname)
            account_id = cursor.fetchone()[0]
            
            # Update accountstats
            cursor.execute("""
                UPDATE accountstats
                SET wepdura = ?, totalload = ?, currentload = ?, x = ?, y = ?
                WHERE accountid = ?
            """, account.wepdura, account.totalload, account.currentload, account.x, account.y, account_id)
            conn.commit()
            
        else:
            # Insert a new account
            cursor.execute("""
                INSERT INTO Account (name, hwnd, threadID, ProcessID, WindowName)
                VALUES (?, ?, ?, ?, ?)
            """, account.charname, account.hwnd, account.threadid, account.processid, account.windowname)
            conn.commit()
                # Get the account ID
            cursor.execute("SELECT accountid FROM Account WHERE name = ?", account.charname)
            account_id = cursor.fetchone()[0]
            # Insert into accountstats
            cursor.execute("""
                UPDATE accountstats
                SET wepdura = ?, totalload = ?, currentload = ?, x = ?, y = ?
                WHERE accountid = ?
            """, account.wepdura, account.totalload, account.currentload,account.x, account.y, account_id)
            conn.commit()
        
        cursor.close()
        conn.close()