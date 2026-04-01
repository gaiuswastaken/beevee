# Libraries
import random
import math
from inventory_manager import *

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
        raise ValueError(f"Probabilities must sum to 1, instead got {total}") # Ensures that the sum of probabilities is always 1 otherwise the logic goes awry
    
    # This is where the weighted selection takes place
    # random_number is used to determine the critical region of the egg, the rarer the bee, the closer to the tails they are
    random_number= random.random()
    cumulative = 0.0
    
    for bee, probability in egg.bees.items():
        cumulative += probability
        if random_number < cumulative:
            # Adds the bee to the inventory
            add_bee_to_inventory(bee)
            # Purely for debugging purposes
            print(f"You hatched: {bee.name}")
            return bee

# Defining the bees
noob_bee = Bee(1, "Noob Bee", "Common")
bumble_bee = Bee(2, "Bumble Bee", "Rare")
overconfident_bee = Bee(3, "Overconfident Bee", "Rare")
happy_bee = Bee(4, "Happy Bee", "Epic")
frustrated_bee = Bee(5, "Frustrated Bee", "Epic")
sleep_deprived_bee = Bee(6, "Sleep-Deprived Bee", "Epic")
chibi_bee = Bee(7, "Chibi Bee", "Legendary")
lion_bee = Bee(8, "Lion Bee", "Legendary")
flame_bee = Bee(9, "Flame Bee", "Mythic")

# Defining the Eggs and the Bees in the eggs as well as their probabilities
# Hardcoding it is not really the best idea but it does prevent unwarranted tampering
starter_egg = Egg("Starter Egg", 1)
starter_egg.add_item(noob_bee, 0.9)
starter_egg.add_item(bumble_bee, 0.05)
starter_egg.add_item(overconfident_bee, 0.05)

rare_egg = Egg("Rare Egg", 2)
rare_egg.add_item(overconfident_bee, 0.35)
rare_egg.add_item(bumble_bee, 0.35)
rare_egg.add_item(happy_bee, 0.1)
rare_egg.add_item(frustrated_bee, 0.1)
rare_egg.add_item(sleep_deprived_bee, 0.1)

epic_egg = Egg("Epic Egg", 3)
epic_egg.add_item(happy_bee, 0.3)
epic_egg.add_item(frustrated_bee, 0.3)
epic_egg.add_item(sleep_deprived_bee, 0.3)
epic_egg.add_item(chibi_bee, 0.05)
epic_egg.add_item(lion_bee, 0.05)

legendary_egg = Egg("Legendary Egg", 4)
legendary_egg.add_item(chibi_bee, 0.45)
legendary_egg.add_item(lion_bee, 0.45)
legendary_egg.add_item(flame_bee, 0.1)

mythic_egg = Egg("Mythic Egg", 5)
mythic_egg.add_item(flame_bee, 1)
