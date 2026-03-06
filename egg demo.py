# Libraries
import random
import math

# Class for the Bee
class Bee:
    # Initialises the class
    def __init__(self, item_id, name, rarity):
        self.id = item_id
        self.name = name
        self.rarity = rarity
        
# Class for the general Egg Class (the acutal buyable eggs will inherit this Class)
class Egg:
    # Initialises the class
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost
        self.bees = {} # A dictionary where the key is the bee and the value is the probability
    
    # A method that adds the bee to their respective egg
    def add_item(self, bee, probability):
        if probability <= 0 or probability > 1:
            raise ValueError("Probability must be between 0 and 1")
        self.bees[bee] = probability
    
    # This method ensures probability adds up to 1 (it is illegal in statistics for the sum of all the probabilities in a distribution to not add up to 1 (either greater than or less than))
    def total_probability(self):
        sigma_probabiliy = sum(self.bees.values())
        return sigma_probabiliy
    
    # This method allows for the purchase of the egg
    def buy(self, balance):
        if balance >= self.cost:
            return True, f"Purchased {self.name}", balance - self.cost
        return False, "Insufficient funds", balance

# This the function that actually allows the egg to be opened and a bee to be hatched
# Tolerance is the margin of uncertainty that is allowed.
# This is because in floating point arithmetic, it is not guaranteed that the probabilities sum up to 1, it may sum up to 0.9999999999999999999999 for instance
# The tolerance is roughly 1x10^-9 which in real world probablilites, is tiny compared to something like 0.1 or 0.001
def open_egg(egg, tolerance=1e-9): 
    total = egg.total_probability()
    if not math.isclose(total, 1.0, abs_tol=tolerance):
        raise ValueError(f"Probabilities must sum to 1, instead got {total}")
    
    # This is where the weighted selection takes place
    # random_number is used to determine the critical region of the egg, the rarer the bee, the closer to the tails they are
    random_number= random.random()
    cumulative = 0.0
    
    for bee, probability in egg.bees.items():
        cumulative += probability
        if random_number < cumulative:
            return bee

# Defining the bees
basic_bee = Bee(1, "Basic Bee", "Common")
bumble_bee = Bee(2, "Bumble Bee", "Rare")
stubborn_bee = Bee(3, "Stubborn Bee", "Rare")
bubble_bee = Bee(4, "Bubble Bee", "Epic")
rage_bee = Bee(5, "Rage Bee", "Epic")
exhausted_bee = Bee(6, "Exhausted Bee", "Epic")
baby_bee = Bee(7, "Baby Bee", "Legendary")
lion_bee = Bee(8, "Lion Bee", "Legendary")
spicy_bee = Bee(9, "Spicy Bee", "Mythic")

# Defining the Eggs and the Bees in the eggs as well as their probabilities
starter_egg = Egg("Starter Egg", 1)
starter_egg.add_item(basic_bee, 0.9)
starter_egg.add_item(bumble_bee, 0.05)
starter_egg.add_item(stubborn_bee, 0.05)

rare_egg = Egg("Rare Egg", 2)
rare_egg.add_item(stubborn_bee, 0.35)
rare_egg.add_item(bumble_bee, 0.35)
rare_egg.add_item(bubble_bee, 0.1)
rare_egg.add_item(rage_bee, 0.1)
rare_egg.add_item(exhausted_bee, 0.1)

epic_egg = Egg("Epic Egg", 3)
epic_egg.add_item(bubble_bee, 0.3)
epic_egg.add_item(rage_bee, 0.3)
epic_egg.add_item(exhausted_bee, 0.3)
epic_egg.add_item(baby_bee, 0.05)
epic_egg.add_item(lion_bee, 0.05)

legendary_egg = Egg("Legendary Egg", 4)
legendary_egg.add_item(baby_bee, 0.45)
legendary_egg.add_item(lion_bee, 0.45)
legendary_egg.add_item(spicy_bee, 0.1)

mythic_egg = Egg("Mythic Egg", 5)
mythic_egg.add_item(spicy_bee, 1)

# Test inventory system - will rework it to SQL Database to store it persistently

inventory = {}

def add_to_inventory(item):
    # Stores the beees by their names instead of objects so the inventory can be stored in plaintext rather than storing it in SQLite as objects,
    # as SQLite does not support storing it as objects (Reference: https://stackoverflow.com/questions/2047814/is-it-possible-to-store-python-class-objects-in-sqlite)
    bee_name = item.name if hasattr(item, 'name') else item # bee_name just extracts the value of the attribute 'name' so that I can achieve what I want to do in the comments above
    inventory[bee_name] = inventory.get(bee_name, 0) + 1
    
# This section is testing only, it will be removed in the final iteration as the GUI will invoke these functions
balance = 100
while True:
    print(f"Balance = {balance}")
    selector = int(input("""Select which egg to buy:
                         1. Starter Egg
                         2. Rare Egg
                         3. Epic Egg
                         4. Legendary Egg
                         5. Mythic Egg
                         6. Quit program"""))
    # Will add validation later
    # The variable 'success' is a flag that only buys the egg if it is 'True'
    if selector == 1:
        success, msg, balance = starter_egg.buy(balance)
        print(msg)
        if success:
            bee = open_egg(starter_egg)
            print(f"You hatched: {bee.name}")
            add_to_inventory(bee)
    elif selector == 2:
        success, msg, balance = rare_egg.buy(balance)
        print(msg)
        if success:
            bee = open_egg(rare_egg)
            print(f"You hatched: {bee.name}")
            add_to_inventory(bee)
    elif selector == 3:
        success, msg, balance = epic_egg.buy(balance)
        print(msg)
        if success:
            bee = open_egg(epic_egg)
            print(f"You hatched: {bee.name}")
            add_to_inventory(bee)
    elif selector == 4:
        success, msg, balance = legendary_egg.buy(balance)
        print(msg)
        if success:
            bee = open_egg(legendary_egg)
            print(f"You hatched: {bee.name}")
            add_to_inventory(bee)
    elif selector == 5:
        success, msg, balance = mythic_egg.buy(balance)
        print(msg)
        if success:
            bee = open_egg(mythic_egg)
            print(f"You hatched: {bee.name}")
            add_to_inventory(bee)
            