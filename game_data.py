"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Xavier Rothwell

AI Usage: ChatGPT assisted with rewriting and integrating exception handling
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError,
    QuestNotFoundError,
    InsufficientLevelError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError
)

# ============================================================================ 
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest file not found: {filename}")

    try:
        with open(filename, "r") as f:
            content = f.read().strip()
    except:
        raise CorruptedDataError("Could not read quest file.")

    if content == "":
        raise InvalidDataFormatError("Quest file is empty.")

    blocks = [b.strip() for b in content.split("\n\n") if b.strip() != ""]

    quests = {}

    for block in blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip() != ""]
        quest_dict = parse_quest_block(lines)
        validate_quest_data(quest_dict)

        # Add default fields for quest management
        quest_dict.setdefault("COMPLETED", False)
        quest_dict.setdefault("ACTIVE", True)

        qid = quest_dict.get("QUEST_ID")
        if not qid:
            raise InvalidDataFormatError("Missing QUEST_ID field.")

        quests[qid] = quest_dict

    return quests


def load_items(filename="data/items.txt"):
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item file not found: {filename}")

    try:
        with open(filename, "r") as f:
            content = f.read().strip()
    except:
        raise CorruptedDataError("Could not read item file.")

    if content == "":
        raise InvalidDataFormatError("Item file is empty.")

    blocks = [b.strip() for b in content.split("\n\n") if b.strip() != ""]

    items = {}

    for block in blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip() != ""]
        item_dict = parse_item_block(lines)
        validate_item_data(item_dict)

        item_id = item_dict.get("ITEM_ID")
        if not item_id:
            raise InvalidDataFormatError("Missing ITEM_ID field.")

        items[item_id] = item_dict

    return items

# ============================================================================ 
# VALIDATION HELPERS
# ============================================================================ 

def validate_quest_data(quest_dict):
    required_fields = [
        "QUEST_ID",
        "TITLE",
        "DESCRIPTION",
        "REWARD_XP",
        "REWARD_GOLD",
        "REQUIRED_LEVEL",
        "PREREQUISITE"
    ]

    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing field: {field}")

    if not isinstance(quest_dict["REWARD_XP"], int):
        raise InvalidDataFormatError("REWARD_XP must be an integer.")
    if not isinstance(quest_dict["REWARD_GOLD"], int):
        raise InvalidDataFormatError("REWARD_GOLD must be an integer.")
    if not isinstance(quest_dict["REQUIRED_LEVEL"], int):
        raise InvalidDataFormatError("REQUIRED_LEVEL must be an integer.")

    return True


def validate_item_data(item_dict):
    required_fields = ["ITEM_ID", "NAME", "TYPE", "EFFECT", "COST", "DESCRIPTION"]

    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing item field: {field}")

    valid_types = ["weapon", "armor", "consumable"]
    if item_dict["TYPE"] not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['TYPE']}")
    if not isinstance(item_dict["COST"], int):
        raise InvalidDataFormatError("Item COST must be an integer")

    return True

# ============================================================================ 
# QUEST MANAGEMENT
# ============================================================================ 

def start_quest(player, quest_id, quests):
    """
    Attempt to start a quest for the player.
    Raises the proper exceptions for failing conditions.
    """
    if quest_id not in quests:
        raise QuestNotFoundError(f"Quest not found: {quest_id}")

    quest = quests[quest_id]

    if player["level"] < quest["REQUIRED_LEVEL"]:
        raise InsufficientLevelError("Your level is too low to start this quest.")

    prereq = quest.get("PREREQUISITE", "NONE")
    if prereq != "NONE" and prereq not in player.get("completed_quests", []):
        raise QuestRequirementsNotMetError("Prerequisite quest not completed.")

    if quest.get("COMPLETED", False) or quest_id in player.get("completed_quests", []):
        raise QuestAlreadyCompletedError("Quest already completed.")

    if not quest.get("ACTIVE", True):
        raise QuestNotActiveError("Quest is not currently active.")

    quest["ACTIVE"] = True
    return True

# ============================================================================ 
# DEFAULT DATA CREATION
# ============================================================================ 

def create_default_data_files():
    os.makedirs("data/save_games", exist_ok=True)

    if not os.path.exists("data/quests.txt"):
        with open("data/quests.txt", "w") as f:
            f.write(
                "QUEST_ID: first_steps\n"
                "TITLE: First Steps\n"
                "DESCRIPTION: Your journey begins.\n"
                "REWARD_XP: 50\n"
                "REWARD_GOLD: 25\n"
                "REQUIRED_LEVEL: 1\n"
                "PREREQUISITE: NONE\n"
            )

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

# ============================================================================ 
# PARSE BLOCKS
# ============================================================================ 

def parse_quest_block(lines):
    quest_info = {}
    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError("Invalid quest line format.")
        key, value = line.split(": ", 1)
        # Keep original key casing
        if key in ["REWARD_XP", "REWARD_GOLD", "REQUIRED_LEVEL"]:
            try:
                value = int(value)
            except:
                raise InvalidDataFormatError(f"Invalid integer for {key}")
        quest_info[key] = value
    return quest_info


def parse_item_block(lines):
    item_info = {}
    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError("Invalid item line format.")
        key, value = line.split(": ", 1)
        if key == "COST":
            try:
                value = int(value)
            except:
                raise InvalidDataFormatError("Invalid COST value")
        item_info[key] = value
    return item_info


