import pyodbc
import json
import os
import re

def get_connection_string(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    
    connection_string = config['database']['connection_string']
    if 'username' in config['database'] and 'password' in config['database']:
        connection_string += f" UID={config['database']['username']}; PWD={config['database']['password']};"
    if config['database'].get('trust_server', False):
        connection_string += " TrustServerCertificate=yes;"
    
    return connection_string

def execute_sql_script(filename, connection_string):
    with open(filename, 'r') as file:
        sql_script = file.read()
    
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql_script)
        conn.commit()
        print(f"SQL script '{filename}' executed successfully.")
    except pyodbc.Error as e:
        print(f"An error occurred while executing '{filename}': {e}")
    finally:
        conn.close()

def main():
    connection_string = get_connection_string('botconfig.json')
    scripts_folder = 'DBUpgrades'
    scripts = [os.path.join(scripts_folder, f) for f in os.listdir(scripts_folder) if f.endswith('.sql')]
    scripts.sort(key=lambda f: int(re.match(r'(\d{3})', os.path.basename(f)).group(1)))
    
    for script in scripts:
        execute_sql_script(script, connection_string)

if __name__ == "__main__":
    main()