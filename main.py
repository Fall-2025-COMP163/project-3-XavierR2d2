"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: Xavier Rothwell

AI Usage: used ai to debug and help format the code

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    print("\n=== MAIN MENU ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")

    choice = input("Enter choice (1-3): ").strip()
    while choice not in ["1","2","3"]:
        choice = input("Enter choice (1-3): ").strip()
    return int(choice)

# ============================================================================ 
# NEW / LOAD GAME
# ============================================================================ 

def new_game():
    global current_character
    load_game_data()

    print("\n=== NEW GAME ===")
    name = input("Enter your character name: ").strip()

    print("\nChoose a class:")
    print("1. Warrior\n2. Mage\n3. Rogue\n4. Cleric")

    class_choice = input("Enter choice (1-4): ").strip()
    while class_choice not in ["1","2","3","4"]:
        class_choice = input("Enter choice (1-4): ").strip()

    class_map = {"1":"Warrior","2":"Mage","3":"Rogue","4":"Cleric"}
    char_class = class_map[class_choice]

    try:
        current_character = character_manager.create_character(name, char_class)
        character_manager.save_character(current_character)
    except InvalidCharacterClassError:
        print("Invalid class.")
        return

    game_loop()

def load_game():
    global current_character
    load_game_data()

    print("\n=== LOAD GAME ===")
    saved_chars = character_manager.list_saved_characters()
    if not saved_chars:
        print("No saved characters found.")
        return

    for i, name in enumerate(saved_chars, 1):
        print(f"{i}. {name}")

    choice = input("Pick a character number: ").strip()
    while not choice.isdigit() or int(choice) < 1 or int(choice) > len(saved_chars):
        choice = input("Pick a character number: ").strip()

    char_name = saved_chars[int(choice)-1]

    try:
        current_character = character_manager.load_character(char_name)
    except (CharacterNotFoundError, SaveFileCorruptedError, InvalidSaveDataError):
        print("Error loading save.")
        return

    game_loop()

# ============================================================================ 
# GAME LOOP
# ============================================================================ 

def game_loop():
    global game_running
    game_running = True

    while game_running:
        choice = game_menu()
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Goodbye.")
            game_running = False

def game_menu():
    print("\n=== GAME MENU ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore")
    print("5. Shop")
    print("6. Save and Quit")

    choice = input("Enter choice (1-6): ").strip()
    while choice not in ["1","2","3","4","5","6"]:
        choice = input("Enter choice (1-6): ").strip()
    return int(choice)

# ============================================================================ 
# CHARACTER AND INVENTORY
# ============================================================================ 

def view_character_stats():
    c = current_character
    print("\n=== CHARACTER STATS ===")
    print(f"Name: {c['name']}")
    print(f"Class: {c['class']}")
    print(f"Level: {c['level']}")
    print(f"Health: {c['health']}/{c['max_health']}")
    print(f"Strength: {c['strength']}")
    print(f"Magic: {c['magic']}")
    print(f"Gold: {c['gold']}")
    print(f"XP: {c['experience']}")
    print(f"Active Quests: {len(c['active_quests'])}")
    print(f"Completed Quests: {len(c['completed_quests'])}")

def view_inventory():
    global current_character, all_items
    print("\n=== INVENTORY ===")
    inventory_system.display_inventory(current_character, all_items)

    print("\nOptions:\n1. Use\n2. Drop\n3. Equip Weapon\n4. Equip Armor\n5. Back")
    choice = input("Choose: ").strip()

    if choice == "1":
        item_id = input("Enter item_id: ").strip()
        try:
            inventory_system.use_item(current_character, item_id, all_items[item_id])
        except Exception as e:
            print(f"Error: {e}")
    elif choice == "2":
        item_id = input("Enter item_id: ").strip()
        try:
            inventory_system.remove_item_from_inventory(current_character, item_id)
        except Exception as e:
            print(f"Error: {e}")
    elif choice == "3":
        item_id = input("Enter weapon_id: ").strip()
        try:
            inventory_system.equip_weapon(current_character, item_id, all_items[item_id])
        except Exception as e:
            print(f"Error: {e}")
    elif choice == "4":
        item_id = input("Enter armor_id: ").strip()
        try:
            inventory_system.equip_armor(current_character, item_id, all_items[item_id])
        except Exception as e:
            print(f"Error: {e}")

# ============================================================================ 
# QUESTS
# ============================================================================ 

def quest_menu():
    global current_character, all_quests
    print("\n=== QUEST MENU ===")
    print("1. Active\n2. Available\n3. Completed\n4. Accept\n5. Abandon\n6. Complete\n7. Back")
    choice = input("Choose: ").strip()

    if choice == "1":
        active = quest_handler.get_active_quests(current_character, all_quests)
        for q in active: quest_handler.display_quest_info(q)
    elif choice == "2":
        available = quest_handler.get_available_quests(current_character, all_quests)
        quest_handler.display_quest_list(available)
    elif choice == "3":
        completed = quest_handler.get_completed_quests(current_character, all_quests)
        for q in completed: quest_handler.display_quest_info(q)
    elif choice == "4":
        qid = input("Enter quest_id: ").strip()
        try:
            quest_handler.accept_quest(current_character, qid, all_quests)
            print("Quest accepted.")
        except Exception as e:
            print(f"Error: {e}")
    elif choice == "5":
        qid = input("Enter quest_id: ").strip()
        try:
            quest_handler.abandon_quest(current_character, qid)
            print("Quest abandoned.")
        except Exception as e:
            print(f"Error: {e}")
    elif choice == "6":
        qid = input("Enter quest_id: ").strip()
        try:
            rewards = quest_handler.complete_quest(current_character, qid, all_quests)
            print("Quest completed.")
            print(f"XP: {rewards['xp']}, Gold: {rewards['gold']}")
        except Exception as e:
            print(f"Error: {e}")

# ============================================================================ 
# EXPLORATION / COMBAT
# ============================================================================ 

def explore():
    global current_character
    print("\nYou explore the area...")
    enemy = combat_system.get_random_enemy_for_level(current_character["level"])
    print(f"A wild {enemy['name']} appears.")

    battle = combat_system.SimpleBattle(current_character, enemy)
    try:
        result = battle.start_battle()
        print(f"Gained {result['xp_gained']} XP and {result['gold_gained']} gold.")
    except CharacterDeadError:
        handle_character_death()

# ============================================================================ 
# SHOP
# ============================================================================ 

def shop():
    global current_character, all_items
    print("\n=== SHOP ===")
    print(f"You have {current_character['gold']} gold.\n")
    for item_id, data in all_items.items():
        print(f"{item_id}: {data['name']} - {data['cost']} gold")

    print("\nOptions:\n1. Buy\n2. Sell\n3. Back")
    choice = input("Choose: ").strip()

    if choice == "1":
        item_id = input("Enter item_id: ").strip()
        try:
            inventory_system.purchase_item(current_character, item_id, all_items[item_id])
            print("Purchase successful.")
        except Exception as e:
            print(f"Error: {e}")
    elif choice == "2":
        item_id = input("Enter item_id: ").strip()
        try:
            gold = inventory_system.sell_item(current_character, item_id, all_items[item_id])
            print(f"Sold for {gold} gold.")
        except Exception as e:
            print(f"Error: {e}")

# ============================================================================ 
# SAVE / LOAD DATA
# ============================================================================ 

def save_game():
    global current_character
    if current_character is None:
        print("No character to save.")
        return
    try:
        character_manager.save_character(current_character)
        print("Game saved.")
    except Exception:
        print("Error saving game.")

def load_game_data():
    global all_quests, all_items
    try:
        all_quests = game_data.load_quests("data/quests.txt")
        all_items = game_data.load_items("data/items.txt")
    except MissingDataFileError:
        game_data.create_default_data_files()
        all_quests = game_data.load_quests("data/quests.txt")
        all_items = game_data.load_items("data/items.txt")
    except InvalidDataFormatError:
        all_quests = {}
        all_items = {}

# ============================================================================ 
# CHARACTER DEATH
# ============================================================================ 

def handle_character_death():
    global current_character, game_running
    print("\nYou died.\n1. Revive for 25 gold\n2. Quit")
    choice = input("Choose: ").strip()
    while choice not in ["1","2"]:
        choice = input("Choose: ").strip()
    if choice == "1":
        if current_character["gold"] < 25:
            print("Not enough gold. Game over.")
            game_running = False
            return
        current_character["gold"] -= 25
        character_manager.revive_character(current_character)
        print("Revived.")
    else:
        print("Goodbye.")
        game_running = False

# ============================================================================ 
# START
# ============================================================================ 

def display_welcome():
    print("="*50)
    print("QUEST CHRONICLES")
    print("="*50)
    print("Welcome to Quest Chronicles.\n")

def main():
    display_welcome()
    load_game_data()
    while True:
        choice = main_menu()
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("Thanks for playing.")
            break

if __name__ == "__main__":
    main()
