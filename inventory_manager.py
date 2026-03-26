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
    object_bee_in_db_search = cursor.execute('''SELECT count FROM inventory WHERE beeName = (?)''', (bee,))
    # Converts the bee object into text where it can be validated and manipulated
    text_bee_in_db_search = object_bee_in_db_search.fetchone()
    if text_bee_in_db_search == None: # If the bee is not present
        print(bees[bee]["rarity"])
        values = [(bee, bees[bee]["rarity"], 1)]
        cursor.executemany("INSERT INTO inventory (beeName, beeRarity, count) VALUES (?, ?, ?)", values)
    else: # Bee is present
        cursor.execute("UPDATE inventory SET count = count + 1 WHERE beeName = ? ", (bee,))
    conn.commit()
    conn.close()