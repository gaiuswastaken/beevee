# Libraries
import sqlite3

# Dictionary Mappings 
# Hardcoding the dictionary may not be the best solution but it makes accessing it faster 
# (in the future, may make it a JSON file that way, it is easier to edit but this future solution runs the risk of unwarranted edititng)
bees = {
    "Basic Bee": {"rarity": "Common"},
    "Bumble Bee": {"rarity": "Rare"},
    "Stubborn Bee": {"rarity": "Rare"},
    "Bubble Bee": {"rarity": "Epic"},
    "Rage Bee": {"rarity": "Epic"},
    "Exhausted Bee": {"rarity": "Epic"},
    "Baby Bee": {"rarity": "Legendary"},
    "Lion Bee": {"rarity": "Legendary"},
    "Spicy Bee": {"rarity": "Mythic"}
}

def create_inventory():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                beeName TEXT PRIMARY KEY,
                beeRarity TEXT NOT NULL,
                count INTEGER NOT NULL
            )
        ''')
    conn.commit()
    conn.close()
    

def add_bee_to_inventory(bee):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    object_bee_in_db_search = cursor.execute('''SELECT count FROM inventory WHERE beeName = (?)''', (bee,))
    text_bee_in_db_search = object_bee_in_db_search.fetchone()
    if text_bee_in_db_search == None:
        cursor.execute("UPDATE inventory SET beeName = ?, rarity = ? , count = 1", (bee,))

    conn.close()

create_inventory()
add_bee_to_inventory("Basic Bee")