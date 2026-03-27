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
def create_index():
    conn = sqlite3.connect("index.db")
    cursor = conn.cursor()
    # Also conducts a sanity check to see if there isnt a table called index (this prevents unnecessary overwriting of data, which could lead to data loss)
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS beeIndex (
                beeName TEXT PRIMARY KEY,
                beeRarity TEXT NOT NULL,
                discovered TEXT NOT NULL
            )
        ''')
    conn.commit()
    conn.close()
    

# Allows for the index to be built when the onboarding screen is launched
def build_index():
    conn = sqlite3.connect("index.db")
    cursor = conn.cursor()
    for bee in range(len(bees)):
        bee = list(bees.keys())[bee]
        values = [(bee, bees[bee]["rarity"], str(False))]
        cursor.executemany("INSERT INTO beeIndex (beeName, beeRarity, discovered) VALUES (?, ?, ?)", values)
    conn.commit()
    conn.close()

# Updates the value of the bees to be discovered to True
def discover_bee(bee):
    conn = sqlite3.connect("index.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE beeIndex SET discovered = ? WHERE beeName = ?", (str(True), bee))
    conn.commit()
    conn.close()

# Returns the list of bees - useful for the Index page in the main screen as I will separate them from discovered and undiscovered
def get_bees_from_index():
    conn = sqlite3.connect("index.db")
    cursor = conn.cursor()
    cursor.execute("SELECT beeName FROM beeIndex")
    available_bees = cursor.fetchall()
    conn.close()
    return available_bees