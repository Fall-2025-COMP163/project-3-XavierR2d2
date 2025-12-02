"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: Xavier Rothwell

AI Usage: chat again helped with the debuging and formating of the code

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):

    inventory = character["inventory"]

    # check if the inventory is full
    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")

    # add item
    inventory.append(item_id)

    return True
    pass

def remove_item_from_inventory(character, item_id):

      """Remove an item from the character's inventory."""

    inventory = character["inventory"]

    # make sure the item is actually in the list
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item not found: {item_id}")

    inventory.remove(item_id)

    return True

    pass

def has_item(character, item_id):

    inventory = character["inventory"]
    
    return item_id in inventory


    pass

def count_item(character, item_id):
    inventory = character["inventory"]

    return inventory.count(item_id)

    pass

def get_inventory_space_remaining(character):

    inventory = character["inventory"]

    # calculate remaining space
    remaining = MAX_INVENTORY_SIZE - len(inventory)

    return remaining
    pass

def clear_inventory(character):

    old_items = character["inventory"].copy()   # save what was there
    
    character["inventory"].clear()              # empty the inventory
    
    return old_items

    pass

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):

    inventory = character["inventory"]

    if item_id not in inventory:
        raise ItemNotFoundError(f"Item not found: {item_id}") # make sure they have the item

    if item_data["type"] != "consumable":
        raise InvalidItemTypeError("Item is not a consumable.") # only consumables can be "used"

    effect_tuple = item_data["effect"] # effect looks like: "health:20"

    stat_name, value = parse_item_effect(effect_tuple)

    apply_stat_effect(character, stat_name, value) # apply the effect to the character

    inventory.remove(item_id) # remove the item after using it

    return f"You used {item_id} and gained {stat_name} +{value}."

    pass

def equip_weapon(character, item_id, item_data):

    inventory = character["inventory"]

    # make sure item is in inventory
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item not found: {item_id}")

    # make sure it is the correct item type
    if item_data["type"] != "weapon":
        raise InvalidItemTypeError("Item is not a weapon.")

    # if a weapon is already equipped, unequip it
    if "equipped_weapon" in character and character["equipped_weapon"] is not None:

        old_weapon = character["equipped_weapon"]
        old_effect = character["equipped_weapon_effect"]    

        # reverse the old weapon's stat effect
        stat_name, value = parse_item_effect(old_effect)
        apply_stat_effect(character, stat_name, -value)      # subtract bonus

        # add old weapon back to inventory
        inventory.append(old_weapon)

    # parse the new weapon's effect
    effect_string = item_data["effect"]   # example: "strength:5"
    stat_name, value = parse_item_effect(effect_string)

    # apply stat bonus
    apply_stat_effect(character, stat_name, value)

    # store equipped data on character
    character["equipped_weapon"] = item_id
    character["equipped_weapon_effect"] = effect_string

    # remove new weapon from inventory
    inventory.remove(item_id)

    return f"You equipped {item_id} (+{stat_name} {value})."

    pass

def equip_armor(character, item_id, item_data):
    inventory = character["inventory"]

    # check item is actually in inventory because you cant add whats not there
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item not found: {item_id}")

    # check that item type is correct
    if item_data["type"] != "armor":
        raise InvalidItemTypeError("Item is not armor.")

    # if armor is already equipped, unequip it first
    if "equipped_armor" in character and character["equipped_armor"] is not None: # not empty meanning somehting is there

        old_armor = character["equipped_armor"]
        old_effect = character["equipped_armor_effect"]

        # reverse old armor bonus
        stat_name, value = parse_item_effect(old_effect)
        apply_stat_effect(character, stat_name, -value)   # subtract the old bonus

        # return old armor to inventory
        inventory.append(old_armor)

    # parse new armor effect (example: "max_health:10")
    effect_string = item_data["effect"]
    stat_name, value = parse_item_effect(effect_string)

    # apply bonus
    apply_stat_effect(character, stat_name, value)

    # save equipped armor info on character
    character["equipped_armor"] = item_id
    character["equipped_armor_effect"] = effect_string

    # remove armor from inventory
    inventory.remove(item_id)

    return f"You equipped {item_id} (+{stat_name} {value})."
    pass

def unequip_weapon(character):

    inventory = character["inventory"]

    # check if a weapon is even equipped
    if "equipped_weapon" not in character or character["equipped_weapon"] is None:
        return None   # nothing to unequip

    weapon_id = character["equipped_weapon"]
    effect = character["equipped_weapon_effect"]

    # make sure inventory has space
    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")

    # reverse the weapon's stat bonus
    stat_name, value = parse_item_effect(effect)
    apply_stat_effect(character, stat_name, -value)   # subtract bonus

    # add weapon back to inventory
    inventory.append(weapon_id)

    # remove equipped info
    character["equipped_weapon"] = None
    character["equipped_weapon_effect"] = None

    return weapon_id
    pass

def unequip_armor(character):

    inventory = character["inventory"]

    # check if armor is even equipped
    if "equipped_armor" not in character or character["equipped_armor"] is None:
        return None   # nothing to unequip

    armor_id = character["equipped_armor"]
    effect = character["equipped_armor_effect"]   # example: "max_health:10"

    # check if there is space in inventory
    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")

    # reverse the armor's stat bonus
    stat_name, value = parse_item_effect(effect)
    apply_stat_effect(character, stat_name, -value)   # subtract bonus

    # add old armor back to inventory
    inventory.append(armor_id)

    # clear equipped armor fields
    character["equipped_armor"] = None
    character["equipped_armor_effect"] = None

    return armor_id
    # TODO: Implement armor unequipping
    pass

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):

    cost = item_data["cost"]
    inventory = character["inventory"]

    # check gold
    if character["gold"] < cost:
        raise InsufficientResourcesError("Not enough gold to purchase this item.")

    # check inventory space
    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")

    # subtract gold
    character["gold"] -= cost

    # 4. Add item to inventory
    inventory.append(item_id)

    return True
    pass

def sell_item(character, item_id, item_data):

    inventory = character["inventory"]

    # tem must be in inventory
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item not found: {item_id}")

    # calculate sell price (half cost, integer division)
    sell_price = item_data["cost"] // 2

    # remove item from inventory
    inventory.remove(item_id)

    # add gold to character
    character["gold"] += sell_price

    return sell_price

    pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    
    if ":" not in effect_string:
        raise InvalidItemTypeError("Invalid effect format.")

    stat_name, value_str = effect_string.split(":", 1) #make sure it only does it one time

    try:
        value = int(value_str)
    except:
        raise InvalidItemTypeError("Effect value must be an integer.")

    return stat_name, value

    pass

def apply_stat_effect(character, stat_name, value):
    # whatever the stat name is will have the value increased by it
    character[stat_name] += value

    # make sure health doesnt get above the max health
    if stat_name == "health":
        if character["health"] > character["max_health"]:
            character["health"] = character["max_health"]    
    pass

def display_inventory(character, item_data_dict):
    """Shows item names, types, and quantities"""
    inventory = character["inventory"]

    if len(inventory) == 0:
        print("Inventory is empty.")
        return

    # Count items (because duplicates may exist)
    item_counts = {}
    for item_id in inventory:
        if item_id not in item_counts:
            item_counts[item_id] = 0
        item_counts[item_id] += 1

    print("=== INVENTORY ===")

    # Display each item with name, type, and quantity
    for item_id, count in item_counts.items():

        # look up item info from item_data_dict
        item_info = item_data_dict.get(item_id, None)

        if item_info is None:
            # in case item ID isn't in the item database
            print(f"{item_id} x{count} (Unknown item)")
            continue

        name = item_info["name"]
        item_type = item_info["type"]

        print(f"{name} ({item_type}) x{count}")
    pass

