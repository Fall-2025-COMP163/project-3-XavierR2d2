"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

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
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    print("\n=== MAIN MENU ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")

    # get input from the user
    choice = input("Enter choice (1-3): ").strip()

    # keep asking until the input is valid
    while choice not in ["1", "2", "3"]:
        print("Invalid choice. Please pick 1, 2, or 3.")
        choice = input("Enter choice (1-3): ").strip()

    return int(choice)
    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice
    pass

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    
    global current_character
    print("\n=== NEW GAME ===")
    
    # get character name
    name = input("Enter your character name: ").strip()

    # choose a class
    print("\nChoose a class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")
    print("4. Cleric")

    class_choice = input("Enter choice (1-4): ").strip()

    # keep asking until valid input
    while class_choice not in ["1", "2", "3", "4"]:
        print("Invalid choice. Pick 1-4.")
        class_choice = input("Enter choice (1-4): ").strip()

    class_map = {
        "1": "Warrior",
        "2": "Mage",
        "3": "Rogue",
        "4": "Cleric"
    }

    character_class = class_map[class_choice]

    # try to make the character
    try:
        current_character = character_manager.create_character(name, character_class)
        character_manager.save_character(current_character)
        print(f"\nCharacter {name} the {character_class} created!")
    except InvalidCharacterClassError:
        print("Error creating character. Class not recognized.")
        return

    # start the game loop
    game_loop()
    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop
    pass

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop
    pass

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    print("\n=== LOAD GAME ===")

    saved = character_manager.list_saved_characters()

    if len(saved) == 0:
        print("No saved characters found.")
        return

    print("Saved Characters:")
    for i, name in enumerate(saved, 1):
        print(f"{i}. {name}")

    choice = input("Pick a character number: ").strip()

    # validate user input
    while not choice.isdigit() or int(choice) < 1 or int(choice) > len(saved):
        print("Invalid selection.")
        choice = input("Pick a character number: ").strip()

    char_name = saved[int(choice) - 1]

    try:
        current_character = character_manager.load_character(char_name)
        print(f"\nLoaded {char_name}!")
    except CharacterNotFoundError:
        print("Save file missing.")
        return
    except SaveFileCorruptedError:
        print("Save file is corrupted.")
        return
    except InvalidSaveDataError:
        print("Save file has invalid data.")
        return

    game_loop()
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action
    pass
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
            print("Game saved. Goodbye!")
            game_running = False
            
def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    print("\n=== GAME MENU ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore")
    print("5. Shop")
    print("6. Save and Quit")

    choice = input("Enter choice (1-6): ").strip()

    while choice not in ["1", "2", "3", "4", "5", "6"]:
        print("Invalid choice.")
        choice = input("Enter choice (1-6): ").strip()

    return int(choice)
    # TODO: Implement game menu
    pass

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character

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
    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler
    pass

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    print("\n=== INVENTORY ===")
    inventory_system.display_inventory(current_character, all_items)

    print("\nOptions:")
    print("1. Use an item")
    print("2. Drop an item")
    print("3. Equip weapon")
    print("4. Equip armor")
    print("5. Back")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        item_id = input("Enter item_id to use: ").strip()
        if item_id not in current_character["inventory"]:
            print("Item not in inventory.")
            return
        try:
            result = inventory_system.use_item(current_character, item_id, all_items[item_id])
            print(result)
        except Exception as e:
            print(f"Error: {e}")

    elif choice == "2":
        item_id = input("Enter item_id to drop: ").strip()
        try:
            inventory_system.remove_item_from_inventory(current_character, item_id)
            print("Item dropped.")
        except Exception as e:
            print(f"Error: {e}")

    elif choice == "3":
        item_id = input("Enter weapon_id to equip: ").strip()
        try:
            result = inventory_system.equip_weapon(current_character, item_id, all_items[item_id])
            print(result)
        except Exception as e:
            print(f"Error: {e}")

    elif choice == "4":
        item_id = input("Enter armor_id to equip: ").strip()
        try:
            result = inventory_system.equip_armor(current_character, item_id, all_items[item_id])
            print(result)
        except Exception as e:
            print(f"Error: {e}")
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system
    pass

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    print("\n=== QUEST MENU ===")
    print("1. View Active Quests")
    print("2. View Available Quests")
    print("3. View Completed Quests")
    print("4. Accept Quest")
    print("5. Abandon Quest")
    print("6. Complete Quest (testing)")
    print("7. Back")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        active = quest_handler.get_active_quests(current_character, all_quests)
        for q in active:
            quest_handler.display_quest_info(q)

    elif choice == "2":
        available = quest_handler.get_available_quests(current_character, all_quests)
        for q in available:
            quest_handler.display_quest_list([q])

    elif choice == "3":
        completed = quest_handler.get_completed_quests(current_character, all_quests)
        for q in completed:
            quest_handler.display_quest_info(q)

    elif choice == "4":
        quest_id = input("Enter quest_id to accept: ").strip()
        try:
            quest_handler.accept_quest(current_character, quest_id, all_quests)
            print("Quest accepted!")
        except Exception as e:
            print(f"Error: {e}")

    elif choice == "5":
        quest_id = input("Enter quest_id to abandon: ").strip()
        try:
            quest_handler.abandon_quest(current_character, quest_id)
            print("Quest abandoned.")
        except Exception as e:
            print(f"Error: {e}")

    elif choice == "6":
        quest_id = input("Enter quest_id to complete: ").strip()
        try:
            rewards = quest_handler.complete_quest(current_character, quest_id, all_quests)
            print("Quest completed!")
            print(f"XP gained: {rewards['xp']}")
            print(f"Gold gained: {rewards['gold']}")
        except Exception as e:
            print(f"Error: {e}")
    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler
    pass

def explore():
    """Find and fight random enemies"""
    global current_character
    print("\nYou explore the area...")

    # pick an enemy based on your level
    enemy = combat_system.get_random_enemy_for_level(current_character["level"])

    print(f"A wild {enemy['name']} appears!")

    battle = combat_system.SimpleBattle(current_character, enemy)

    try:
        result = battle.start_battle()
        print(f"You defeated the enemy!")
        print(f"Gained {result['xp_gained']} XP and {result['gold_gained']} gold.")
    except CharacterDeadError:
        handle_character_death()
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions
    pass

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    print("\n=== SHOP ===")
    print(f"You have {current_character['gold']} gold.\n")

    print("Items for sale:")
    for item_id, data in all_items.items():
        print(f"{item_id}: {data['name']} - {data['cost']} gold")

    print("\nOptions:")
    print("1. Buy Item")
    print("2. Sell Item")
    print("3. Back")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        item_id = input("Enter the item_id you want to buy: ").strip()
        if item_id not in all_items:
            print("Item does not exist.")
            return
        try:
            inventory_system.purchase_item(current_character, item_id, all_items[item_id])
            print("Purchase successful!")
        except Exception as e:
            print(f"Error: {e}")

    elif choice == "2":
        item_id = input("Enter the item_id you want to sell: ").strip()
        if item_id not in current_character["inventory"]:
            print("You do not have this item.")
            return
        try:
            gold = inventory_system.sell_item(current_character, item_id, all_items[item_id])
            print(f"Sold for {gold} gold.")
        except Exception as e:
            print(f"Error: {e}")
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system
    pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    if current_character is None:
        print("No character to save.")
        return

    try:
        character_manager.save_character(current_character)
        print("Game saved successfully!")
    except Exception:
        print("Error saving game.")
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions
    pass

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except MissingDataFileError:
        print("Data files missing. Creating defaults...")
        game_data.create_default_data_files()
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except InvalidDataFormatError as e:
        print(f"Invalid data format: {e}")
    except CorruptedDataError:
        print("Data file is corrupted.")
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()
    pass

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    print("\n=== YOU DIED ===")
    print("1. Revive (costs 25 gold)")
    print("2. Quit game")

    choice = input("Choose an option: ").strip()

    while choice not in ["1", "2"]:
        print("Invalid choice.")
        choice = input("Choose an option: ").strip()

    if choice == "1":
        if current_character["gold"] < 25:
            print("Not enough gold to revive. Game over.")
            game_running = False
            return

        # pay revive cost
        current_character["gold"] -= 25
        character_manager.revive_character(current_character)
        print("You have been revived!")
    else:
        print("Goodbye....")
        game_running = False
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False
    pass

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

