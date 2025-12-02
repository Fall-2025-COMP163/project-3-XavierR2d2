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

    blocks = [b.strip() for b in content.split("\n\n") if b.strip()]
    quests = {}

    for block in blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        quest = parse_quest_block(lines)
        validate_quest_data(quest)

        quest_id = quest.get("QUEST_ID")
        if not quest_id:
            raise InvalidDataFormatError("Missing quest_id field.")

        # Initialize quest state
        quest.setdefault("ACTIVE", True)
        quest.setdefault("COMPLETED", False)

        quests[quest_id] = quest

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

    blocks = [b.strip() for b in content.split("\n\n") if b.strip()]
    items = {}

    for block in blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        item = parse_item_block(lines)
        validate_item_data(item)

        item_id = item.get("ITEM_ID")
        if not item_id:
            raise InvalidDataFormatError("Missing item_id field.")

        items[item_id] = item

    return items


# ============================================================================ 
# VALIDATION HELPERS
# ============================================================================ 

def validate_quest_data(quest):
    required = ["QUEST_ID", "TITLE", "DESCRIPTION", "REWARD_XP", "REWARD_GOLD", "REQUIRED_LEVEL", "PREREQUISITE"]
    for field in required:
        if field not in quest:
            raise InvalidDataFormatError(f"Missing field: {field}")

    for key in ["REWARD_XP", "REWARD_GOLD", "REQUIRED_LEVEL"]:
        if not isinstance(quest[key], int):
            raise InvalidDataFormatError(f"{key} must be an integer")

    return True


def validate_item_data(item):
    required = ["ITEM_ID", "NAME", "TYPE", "EFFECT", "COST", "DESCRIPTION"]
    for field in required:
        if field not in item:
            raise InvalidDataFormatError(f"Missing field: {field}")

    if item["TYPE"] not in ["weapon", "armor", "consumable"]:
        raise InvalidDataFormatError(f"Invalid item type: {item['TYPE']}")

    if not isinstance(item["COST"], int):
        raise InvalidDataFormatError("COST must be integer")

    return True


# ============================================================================ 
# PARSING HELPERS
# ============================================================================ 

def parse_quest_block(lines):
    quest = {}
    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError("Invalid quest line format")
        key, value = line.split(": ", 1)
        key = key.strip().upper()
        value = value.strip()
        if key in ["REWARD_XP", "REWARD_GOLD", "REQUIRED_LEVEL"]:
            try:
                value = int(value)
            except:
                raise InvalidDataFormatError(f"{key} must be an integer")
        quest[key] = value
    return quest


def parse_item_block(lines):
    item = {}
    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError("Invalid item line format")
        key, value = line.split(": ", 1)
        key = key.strip().upper()
        value = value.strip()
        if key == "COST":
            try:
                value = int(value)
            except:
                raise InvalidDataFormatError("COST must be integer")
        item[key] = value
    return item


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
# QUEST MANAGEMENT
# ============================================================================ 

def accept_quest(player, quest_id, quests):
    if quest_id not in quests:
        raise QuestNotFoundError(f"Quest not found: {quest_id}")

    quest = quests[quest_id]

    if player["level"] < quest["REQUIRED_LEVEL"]:
        raise InsufficientLevelError("Player level too low.")

    prereq = quest.get("PREREQUISITE", "NONE")
    if prereq != "NONE" and prereq not in player.get("completed_quests", []):
        raise QuestRequirementsNotMetError("Prerequisite not completed.")

    if quest_id in player.get("completed_quests", []):
        raise QuestAlreadyCompletedError("Quest already completed.")

    if not quest.get("ACTIVE", True):
        raise QuestNotActiveError("Quest not active.")

    player.setdefault("active_quests", [])
    if quest_id not in player["active_quests"]:
        player["active_quests"].append(quest_id)

    quest["ACTIVE"] = True
    return True


def complete_quest(player, quest_id, quests):
    if quest_id not in quests:
        raise QuestNotFoundError(f"Quest not found: {quest_id}")

    quest = quests[quest_id]

    if quest_id not in player.get("active_quests", []):
        raise QuestNotActiveError("Quest not active.")

    player["xp"] += quest["REWARD_XP"]
    player["gold"] += quest["REWARD_GOLD"]

    player["active_quests"].remove(quest_id)
    player.setdefault("completed_quests", [])
    player["completed_quests"].append(quest_id)

    quest["COMPLETED"] = True
    quest["ACTIVE"] = False
    return True


def is_quest_completed(player, quest_id):
    return quest_id in player.get("completed_quests", [])


def can_accept_quest(player, quest_id, quests):
    if quest_id not in quests:
        return False
    quest = quests[quest_id]

    if player["level"] < quest["REQUIRED_LEVEL"]:
        return False

    prereq = quest.get("PREREQUISITE", "NONE")
    if prereq != "NONE" and prereq not in player.get("completed_quests", []):
        return False

    if quest_id in player.get("completed_quests", []):
        return False

    if not quest.get("ACTIVE", True):
        return False

    return True


