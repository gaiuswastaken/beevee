import sqlite3
import os

ABS_PATH = os.path.dirname(os.path.abspath(__file__))

def create_setting(setting):
    DB_PATH = os.path.join(ABS_PATH, "config.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Also conducts a sanity check to see if there isnt a table called settings (this prevents unnecessary overwriting of data, which could lead to data loss)
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                name TEXT PRIMARY KEY,
                enabled TEXT
            )
        ''')
    values = [(setting, str(False))]
    # The IGNORE part ensures that the Onboarding Screen does not crash if it is relaunched (re-calling the function) if another setting already exists
    cursor.executemany("INSERT OR IGNORE INTO settings (name, enabled) VALUES (?, ?)", values)
    conn.commit()
    conn.close()
    
def get_setting(setting):
    DB_PATH = os.path.join(ABS_PATH, "config.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT enabled FROM settings WHERE name = ?", (setting,))
    value_setting = cursor.fetchall()
    conn.close()
    return value_setting

def enable_setting(setting):
    DB_PATH = os.path.join(ABS_PATH, "config.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE settings SET enabled = ? WHERE name = ?", (str(True), setting))
    conn.commit()
    conn.close()
    
def disable_setting(setting):
    DB_PATH = os.path.join(ABS_PATH, "config.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE settings SET enabled = ? WHERE name = ?", (str(False), setting))
    conn.commit()
    conn.close()

