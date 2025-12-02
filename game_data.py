"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Xavier Rothwell

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    if not os.path.exists(filename): 
        raise MissingDataFileError(f"Quest file not found: {filename}")

     # try reading the file to catch unreadable or corrupted files
    try:
        with open(filename, "r") as f:
            content = f.read().strip()
    except:
        raise CorruptedDataError("Could not read quest file.")
    
    if content == "":
        raise InvalidDataFormatError("Quest file is empty.")
    
    blocks = content.strip().split("\n\n") #seperates the file quests, every time there's two new lines
    quests = {} #empty dictionary to store the quests

    for block in blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip() != ""]
        quest_dict = parse_quest_block(lines) #using other methods to organize it
        validate_quest_data(quest_dict) #makes sure there is no data missing
        quests[quest_dict["quest_id"]] = quest_dict #setting the name of the quest in the dictionary
    
    return quests
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    pass

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # checks if it the file has been created
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item file not found: {filename}")
    
    try:
        with open(filename, "r") as f:
            content = f.read().strip()
    except:
        raise CorruptedDataError("Could not read item file.")
    
    if content == "":
        raise InvalidDataFormatError("Item file is empty.") #Check to see if it s empty

    
    blocks = content.strip().split("\n\n") # code does the same thing as load quests, except with items
    items = {}
    
    for block in blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip() != ""]
        item_dict = parse_item_block(lines)
        validate_item_data(item_dict)
        items[item_dict["item_id"]] = item_dict
    
    return items
    # TODO: Implement this function
    # Must handle same exceptions as load_quests
    pass

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    required_fields = [
        "quest_id",
        "title",
        "description",
        "reward_xp",
        "reward_gold",
        "required_level",
        "prerequisite"
    ]
    
    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing field: {field}") # these have to be in the file, if one is off then it'll get the error
    
    # check that certain fields should be numbers
    if not isinstance(quest_dict["reward_xp"], int):
        raise InvalidDataFormatError("reward_xp must be an integer.")
    
    if not isinstance(quest_dict["reward_gold"], int):
        raise InvalidDataFormatError("reward_gold must be an integer.")
    
    if not isinstance(quest_dict["required_level"], int):
        raise InvalidDataFormatError("required_level must be an integer.")
    
    return True
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers
    pass

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    required_fields = ["item_id", "name", "type", "effect", "cost", "description"] #setting up these as the valid keys that must be in the dictionary or else you get an error
    
    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing item field: {field}")
    
    valid_types = ["weapon", "armor", "consumable"] # does the same thing for the type of item so if the type doesn't match you get the error
    
    if item_dict["type"] not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")
    
    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError("Item cost must be an integer") #cost must be an integer
    
    return True
    # TODO: Implement validation
    pass

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # Make the data directory
    if not os.path.exists("data"):
        os.makedirs("data") #making a new folder, call it data
    
    # Make save_games folder
    if not os.path.exists("data/save_games"):
        os.makedirs("data/save_games") #make save_games file inside the data folder if it doesnt exist

    # Default quests file
    if not os.path.exists("data/quests.txt"):
        with open("data/quests.txt", "w") as f: # make a quests file if it doesnt exist
            f.write(
                "QUEST_ID: first_steps\n"
                "TITLE: First Steps\n"
                "DESCRIPTION: Your journey begins.\n"
                "REWARD_XP: 50\n"
                "REWARD_GOLD: 25\n"
                "REQUIRED_LEVEL: 1\n"
                "PREREQUISITE: NONE\n"
            )

    # Default items file
    if not os.path.exists("data/items.txt"):
        with open("data/items.txt", "w") as f:
            f.write(
                "ITEM_ID: health_potion\n"
                "NAME: Health Potion\n"
                "TYPE: consumable\n"
                "EFFECT: health:20\n"
                "COST: 25\n"
                "DESCRIPTION: Restores 20 HP.\n"
            )
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately
    pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    quest_info = {}
    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError("Invalid quest line format.")# Line was not valid, so return error
        
        key, value = line.split(": ", 1) # splits the key and value and assigns them to variables
        
        key = key.lower()
        
        if key in ["reward_xp", "reward_gold", "required_level"]:
            value = int(value) #convert them into numbers from strings
        
        quest_info[key] = value # add it to the dictionary
    
    return quest_info # return the checked dictionary
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    pass

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    item_info = {} #this code will do the same stuff as parse quest
    
    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError("Invalid item line format.")
        
        key, value = line.split(": ", 1)
        key = key.lower()
        
        if key == "cost":
            value = int(value)
        
        item_info[key] = value
    
    return item_info
    # TODO: Implement parsing logic
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
     create_default_data_files()
    
    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quests")
    except MissingDataFileError:
        print("Quest file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid quest format: {e}")

    try:
        items = load_items()
        print(f"Loaded {len(items)} items")
    except MissingDataFileError:
        print("Item file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid item format: {e}")

