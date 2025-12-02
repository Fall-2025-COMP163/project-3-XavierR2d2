"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Xavier Rothwell

AI Usage: Chat gpt - to help debug and find errors in my code

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    valid_classes = ["Warrior", "Mage", "Rogue", "Cleric"]
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"invalid class: {character_class}")

    class_stats = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15}
    }

    stats = class_stats[character_class]

    character = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }

    return character


def save_character(character, save_directory="data/save_games"):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    filename = os.path.join(save_directory, f"{character['name']}_save.txt")

    try:
        with open(filename, 'w') as f:
            f.write(f"NAME: {character['name']}\n")
            f.write(f"CLASS: {character['class']}\n")
            f.write(f"LEVEL: {character['level']}\n")
            f.write(f"HEALTH: {character['health']}\n")
            f.write(f"MAX_HEALTH: {character['max_health']}\n")
            f.write(f"STRENGTH: {character['strength']}\n")
            f.write(f"MAGIC: {character['magic']}\n")
            f.write(f"EXPERIENCE: {character['experience']}\n")
            f.write(f"GOLD: {character['gold']}\n")

            inv = ",".join(character["inventory"])
            active = ",".join(character["active_quests"])
            done = ",".join(character["completed_quests"])

            f.write(f"INVENTORY: {inv}\n")
            f.write(f"ACTIVE_QUESTS: {active}\n")
            f.write(f"COMPLETED_QUESTS: {done}\n")

        return True

    except:
        raise IOError("error saving character file")


def load_character(character_name, save_directory="data/save_games"):
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"no save file for: {character_name}")

    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except:
        raise SaveFileCorruptedError("could not read save file")

    character = {}

    for line in lines:
        if line.strip() == "":
            continue
        if ": " not in line:
            raise InvalidSaveDataError("invalid line format")

        key, value = line.strip().split(":", 1)
        key = key.lower()
        value = value.strip()

        if key in ["level", "health", "max_health", "strength", "magic", "experience", "gold"]:
            try:
                value = int(value)
            except:
                raise InvalidSaveDataError(f"invalid number for {key}")

        elif key in ["inventory", "active_quests", "completed_quests"]:
            if value == "":
                value = []
            else:
                value = value.split(",")

        character[key] = value

    validate_character_data(character)

    return character


def list_saved_characters(save_directory="data/save_games"):
    if not os.path.exists(save_directory):
        return []

    characters = []
    for filename in os.listdir(save_directory):
        if filename.endswith("_save.txt"):
            characters.append(filename.replace("_save.txt", ""))
    return characters


def delete_character(character_name, save_directory="data/save_games"):
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"no save file for: {character_name}")

    try:
        os.remove(filename)
    except:
        raise SaveFileCorruptedError("could not delete save file")

    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    if character["health"] == 0:
        raise CharacterDeadError("cannot gain xp while dead")

    character["experience"] += xp_amount

    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]

    return True


def add_gold(character, amount):
    new_total = character["gold"] + amount
    if new_total < 0:
        raise ValueError("not enough gold")
    character["gold"] = new_total
    return character["gold"]


def heal_character(character, amount):
    if is_character_dead(character):
        return 0

    start = character["health"]
    new_hp = min(start + amount, character["max_health"])
    character["health"] = new_hp
    return new_hp - start


def is_character_dead(character):
    return character["health"] <= 0


def revive_character(character):
    half = character["max_health"] // 2
    character["health"] = half
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    required_fields = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]

    for field in required_fields:
        if field not in character:
            raise InvalidSaveDataError(f"Missing field: {field}")

    num_fields = ["level", "health", "max_health", "strength", "magic", "experience", "gold"]
    for num in num_fields:
        if not isinstance(character[num], int):
            raise InvalidSaveDataError(f"{num} must be an integer")

    list_fields = ["inventory", "active_quests", "completed_quests"]
    for lst in list_fields:
        if not isinstance(character[lst], list):
            raise InvalidSaveDataError(f"{lst} must be a list")

    return

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")

    try:
        char = create_character("TestHero", "Warrior")
        print(f"Created: {char['name']} the {char['class']}")
        print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    except InvalidCharacterClassError as e:
        print(f"Invalid class: {e}")

    try:
        save_character(char)
        print("Character saved successfully")
    except Exception as e:
        print(f"Save error: {e}")

    try:
        loaded = load_character("TestHero")
        print(f"Loaded: {loaded['name']}")
    except CharacterNotFoundError:
        print("Character not found")
    except SaveFileCorruptedError:
        print("Save file corrupted")
