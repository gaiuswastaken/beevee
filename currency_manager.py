import sqlite3
import random
from datetime import date

def create_honeycomb_currency_db():
    conn = sqlite3.connect("currency.db")
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS currency (
                honeycombs INTEGER
            )
        ''')
    cursor.execute('''INSERT INTO currency (honeycombs) VALUES (?)''', (0,))
    conn.commit()
    conn.close()
    
def get_honeycombs():
    conn = sqlite3.connect("currency.db")
    cursor = conn.cursor()
    cursor.execute("SELECT honeycombs FROM currency LIMIT 1")
    honeycombs = cursor.fetchone()[0]
    conn.close()
    return honeycombs

def update_honeycombs_after_task_completion(amount=20):
    conn = sqlite3.connect("currency.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE currency SET honeycombs = honeycombs + ?", (amount,))
    conn.commit()
    conn.close()

def update_honeycombs_after_starter_egg_purchase(amount=10):
    conn = sqlite3.connect("currency.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE currency SET honeycombs = honeycombs - ?", (amount,))
    conn.commit()
    conn.close()

def update_honeycombs_after_rare_egg_purchase(amount=20):
    conn = sqlite3.connect("currency.db")
    cursor = conn.cursor()  
    cursor.execute("UPDATE currency SET honeycombs = honeycombs - ?", (amount,))
    conn.commit()
    conn.close()
    
def update_honeycombs_after_epic_egg_purchase(amount=30):
    conn = sqlite3.connect("currency.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE currency SET honeycombs = honeycombs - ?", (amount,))
    conn.commit()
    conn.close()

def update_honeycombs_after_legendary_egg_purchase(amount=40):
    conn = sqlite3.connect("currency.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE currency SET honeycombs = honeycombs - ?", (amount,))
    conn.commit()
    conn.close()

def update_honeycombs_after_mythic_egg_purchase(amount=50):
    conn = sqlite3.connect("currency.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE currency SET honeycombs = honeycombs - ?", (amount,))
    conn.commit()
    conn.close()