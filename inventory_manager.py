# Libraries
import sqlite3
from index_manager import discover_bee

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

# Creates the bees inventory
def create_inventory():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    # Also conducts a sanity check to see if there isnt a table called inventory (this prevents unnecessary overwriting of data, which could lead to data loss)
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                beeName TEXT PRIMARY KEY,
                beeRarity TEXT NOT NULL,
                count INTEGER NOT NULL
            )
        ''')
    conn.commit()
    conn.close()
    

# Allows for any bee to be added
def add_bee_to_inventory(bee):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    # Checks if the bee is already present
    object_bee_in_db_search = cursor.execute('''SELECT count FROM inventory WHERE beeName = (?)''', (bee.name,))
    # Converts the bee object into text where it can be validated and manipulated
    text_bee_in_db_search = object_bee_in_db_search.fetchone()
    if text_bee_in_db_search == None: # If the bee is not present
        print(bees[bee.name]["rarity"])
        valuesInventory = [(bee.name, bees[bee.name]["rarity"], 1)]
        # Stores the beees by their names instead of objects so the inventory can be stored in plaintext rather than storing it in SQLite as objects,
        # as SQLite does not support storing it as objects (Reference: https://stackoverflow.com/questions/2047814/is-it-possible-to-store-python-class-objects-in-sqlite)
        discover_bee(bee.name)
        cursor.executemany("INSERT INTO inventory (beeName, beeRarity, count) VALUES (?, ?, ?)", valuesInventory)
        
    else: # Bee is present
        cursor.execute("UPDATE inventory SET count = count + 1 WHERE beeName = ? ", (bee.name,))
    conn.commit()
    conn.close()
    
# Returns the list of bees in inventory - useful for the Inventory page in the main screen as I will dynamically populate it
def get_bees_from_inventory():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT beeName FROM inventory")
    available_bees = cursor.fetchall()
    conn.close()
    return available_bees