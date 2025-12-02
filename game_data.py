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

        qid = quest_dict.get("quest_id")
        if not qid:
            raise InvalidDataFormatError("Missing quest_id field.")

        # default active and completed flags
        quest_dict.setdefault("active", True)
        quest_dict.setdefault("completed", False)

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

        item_id = item_dict.get("item_id")
        if not item_id:
            raise InvalidDataFormatError("Missing item_id field.")

        items[item_id] = item_dict

    return items

# ============================================================================ 
# QUEST OPERATIONS
# ============================================================================

def start_quest(player, quest_id, quests):
    """
    Attempt to start a quest for a player
    """
    if quest_id not in quests:
        raise QuestNotFoundError(f"Quest not found: {quest_id}")

    quest = quests[quest_id]

    if player["level"] < quest["required_level"]:
        raise InsufficientLevelError(f"Player level too low for {quest_id}")

    prereq = quest.get("prerequisite", "NONE")
    if prereq != "NONE" and prereq not in player.get("completed_quests", []):
        raise QuestRequirementsNotMetError(f"Prerequisite {prereq} not completed")

    if quest.get("completed") or quest_id in player.get("completed_quests", []):
        raise QuestAlreadyCompletedError(f"Quest {quest_id} already completed")

    if not quest.get("active", True):
        raise QuestNotActiveError(f"Quest {quest_id} is not active")

    # Mark quest as active for player
    quest["active"] = True
    return quest

# ============================================================================ 
# VALIDATION HELPERS
# ============================================================================

def validate_quest_data(quest_dict):
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
            raise InvalidDataFormatError(f"Missing field: {field}")

    if not isinstance(quest_dict["reward_xp"], int):
        raise InvalidDataFormatError("reward_xp must be an integer.")
    if not isinstance(quest_dict["reward_gold"], int):
        raise InvalidDataFormatError("reward_gold must be an integer.")
    if not isinstance(quest_dict["required_level"], int):
        raise InvalidDataFormatError("required_level must be an integer.")
    return True


def validate_item_data(item_dict):
    required_fields = ["item_id", "name", "type", "effect", "cost", "description"]
    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing item field: {field}")

    valid_types = ["weapon", "armor", "consumable"]
    if item_dict["type"] not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")
    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError("Item cost must be an integer")
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
        key = key.lower()
        if key in ["reward_xp", "reward_gold", "required_level"]:
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
        key = key.lower()
        if key == "cost":
            try:
                value = int(value)
            except:
                raise InvalidDataFormatError("Invalid cost value")
        item_info[key] = value
    return item_info


