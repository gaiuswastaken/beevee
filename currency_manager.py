import sqlite3
import os

ABS_PATH = os.path.dirname(os.path.abspath(__file__))

def create_honeycomb_currency_db():
    DB_PATH = os.path.join(ABS_PATH, "currency.db") 
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS currency (
                honeycombs INTEGER
            )
        ''')
    # A failsafe to ensure that the currency is only created if it doesn't already exist
    cursor.execute("SELECT count(*) FROM currency")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''INSERT INTO currency (honeycombs) VALUES (?)''', (0,))
    conn.commit()
    conn.close()
    
def get_honeycombs():
    DB_PATH = os.path.join(ABS_PATH, "currency.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT honeycombs FROM currency LIMIT 1")
    honeycombs = cursor.fetchone()[0]
    conn.close()
    return honeycombs

def update_honeycombs_after_task_completion(amount=20):
    DB_PATH = os.path.join(ABS_PATH, "currency.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE currency SET honeycombs = honeycombs + ?", (amount,))
    conn.commit()
    conn.close()

def update_honeycombs_after_starter_egg_purchase(amount=200):
    DB_PATH = os.path.join(ABS_PATH, "currency.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE currency SET honeycombs = honeycombs - ?", (amount,))
    conn.commit()
    conn.close()

def update_honeycombs_after_rare_egg_purchase(amount=400):
    DB_PATH = os.path.join(ABS_PATH, "currency.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE currency SET honeycombs = honeycombs - ?", (amount,))
    conn.commit()
    conn.close()
    
def update_honeycombs_after_epic_egg_purchase(amount=800):
    DB_PATH = os.path.join(ABS_PATH, "currency.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE currency SET honeycombs = honeycombs - ?", (amount,))
    conn.commit()
    conn.close()

def update_honeycombs_after_legendary_egg_purchase(amount=1600):
    DB_PATH = os.path.join(ABS_PATH, "currency.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE currency SET honeycombs = honeycombs - ?", (amount,))
    conn.commit()
    conn.close()

def update_honeycombs_after_mythic_egg_purchase(amount=3200):
    DB_PATH = os.path.join(ABS_PATH, "currency.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE currency SET honeycombs = honeycombs - ?", (amount,))
    conn.commit()
    conn.close()