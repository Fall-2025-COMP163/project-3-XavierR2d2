"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: Xavier Rothwell

AI Usage: ai was used to fix and debug code through out the making process.

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)
from character_manager import gain_experience, add_gold
# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest not found: {quest_id}")

    quest = quest_data_dict[quest_id]

    # check level requirement
    if character["level"] < quest["required_level"]:
        raise InsufficientLevelError("Level too low for this quest.")

    # check prerequisite
    prereq = quest["prerequisite"]   # can be "NONE" or another quest
    if prereq != "NONE":
        if prereq not in character["completed_quests"]:
            raise QuestRequirementsNotMetError("Prerequisite quest not completed.")

    # cannot accept a completed quest
    if quest_id in character["completed_quests"]:
        raise QuestAlreadyCompletedError("Quest already completed.")

    # cannot accept if quest already active
    if quest_id in character["active_quests"]:
        raise QuestRequirementsNotMetError("Quest already active.")

    # finally accept
    character["active_quests"].append(quest_id)

    return True
    # TODO: Implement quest acceptance
    # Check quest exists
    # Check level requirement
    # Check prerequisite (if not "NONE")
    # Check not already completed
    # Check not already active
    # Add to character['active_quests']
    pass

def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError("Quest not found.")

    # quest must be active
    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError("Quest is not active.")

    quest = quest_data_dict[quest_id]

    # remove from active
    character["active_quests"].remove(quest_id)

    # add to completed
    character["completed_quests"].append(quest_id)

    # give rewards
    xp = quest["reward_xp"]
    gold = quest["reward_gold"]

    gain_experience(character, xp)
    add_gold(character, gold)

    return {
        "xp_gained": xp,
        "gold_gained": gold
    }
    # TODO: Implement quest completion
    # Check quest exists
    # Check quest is active
    # Remove from active_quests
    # Add to completed_quests
    # Grant rewards (use character_manager.gain_experience and add_gold)
    # Return reward summary
    pass

def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError("Quest is not active.")

    character["active_quests"].remove(quest_id)

    return True
    # TODO: Implement quest abandonment
    pass

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    active_list = []

    for quest_id in character["active_quests"]:
        if quest_id in quest_data_dict:
            active_list.append(quest_data_dict[quest_id])

    return active_list
    # TODO: Implement active quest retrieval
    # Look up each quest_id in character['active_quests']
    # Return list of full quest data dictionaries
    pass

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    completed_list = []

    for quest_id in character["completed_quests"]:
        if quest_id in quest_data_dict:
            completed_list.append(quest_data_dict[quest_id])

    return completed_list
    # TODO: Implement completed quest retrieval
    pass

def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    available = []

    for quest_id, quest in quest_data_dict.items():

        # skip if already completed
        if quest_id in character["completed_quests"]:
            continue

        # skip if already active
        if quest_id in character["active_quests"]:
            continue

        # check level
        if character["level"] < quest["required_level"]:
            continue

        # check prerequisite
        prereq = quest["prerequisite"]
        if prereq != "NONE":
            if prereq not in character["completed_quests"]:
                continue

        # everything is okay
        available.append(quest)

    return available
    # TODO: Implement available quest search
    # Filter all quests by requirements
    pass

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    return quest_id in character["completed_quests"]
    # TODO: Implement completion check
    pass

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    return quest_id in character["completed_quests"]
    # TODO: Implement active check
    pass

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    if quest_id not in quest_data_dict:
        return False

    quest = quest_data_dict[quest_id]

    # already active or done?
    if quest_id in character["active_quests"]:
        return False

    if quest_id in character["completed_quests"]:
        return False

    # level check
    if character["level"] < quest["required_level"]:
        return False

    # prerequisite check
    prereq = quest["prerequisite"]
    if prereq != "NONE" and prereq not in character["completed_quests"]:
        return False

    return True
    # TODO: Implement requirement checking
    # Check all requirements without raising exceptions
    pass

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError("Quest not found.")

    chain = []
    current = quest_id

    while True:
        if current not in quest_data_dict:
            raise QuestNotFoundError("Quest not found in chain.")

        chain.insert(0, current)

        prereq = quest_data_dict[current]["prerequisite"]

        if prereq == "NONE":
            break

        current = prereq

    return chain
    # TODO: Implement prerequisite chain tracing
    # Follow prerequisite links backwards
    # Build list in reverse order
    pass

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    total = len(quest_data_dict)
    done = len(character["completed_quests"])

    if total == 0:
        return 0.0

    percent = (done / total) * 100

    return percent
    # TODO: Implement percentage calculation
    # total_quests = len(quest_data_dict)
    # completed_quests = len(character['completed_quests'])
    # percentage = (completed / total) * 100
    pass

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    total_xp = 0
    total_gold = 0

    for quest_id in character["completed_quests"]:
        if quest_id in quest_data_dict:
            total_xp += quest_data_dict[quest_id]["reward_xp"]
            total_gold += quest_data_dict[quest_id]["reward_gold"]

    return {
        "total_xp": total_xp,
        "total_gold": total_gold
    }
    # TODO: Implement reward calculation
    # Sum up reward_xp and reward_gold for all completed quests
    pass

def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    result = []

    for quest in quest_data_dict.values():
        if quest["required_level"] >= min_level and quest["required_level"] <= max_level:
            result.append(quest)

    return result
    # TODO: Implement level filtering
    pass

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    # TODO: Implement quest display
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print(f"Required Level: {quest_data['required_level']}")
    print(f"Reward: {quest_data['reward_xp']} XP, {quest_data['reward_gold']} Gold")
    print(f"Prerequisite: {quest_data['prerequisite']}")
    # ... etc
    pass

def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    for quest in quest_list:
        print(f"- {quest['title']} (Lvl {quest['required_level']}) XP:{quest['reward_xp']} Gold:{quest['reward_gold']}")
    # TODO: Implement quest list display
    pass

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    total = len(quest_data_dict)
    completed = len(character["completed_quests"])
    percent = get_quest_completion_percentage(character, quest_data_dict)
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)

    print("\n=== QUEST PROGRESS ===")
    print(f"Active quests: {len(character['active_quests'])}")
    print(f"Completed quests: {completed}/{total} ({percent:.2f} percent)")
    print(f"Total XP earned: {rewards['total_xp']}")
    print(f"Total Gold earned: {rewards['total_gold']}")
    # TODO: Implement progress display
    pass

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    for quest_id, quest in quest_data_dict.items():
        prereq = quest["prerequisite"]

        if prereq != "NONE":
            if prereq not in quest_data_dict:
                raise QuestNotFoundError(f"Invalid prerequisite: {prereq}")

    return True
    # TODO: Implement prerequisite validation
    # Check each quest's prerequisite
    # Ensure prerequisite exists in quest_data_dict
    pass


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    test_char = {
        'level': 1,
        'active_quests': [],
        'completed_quests': [],
        'experience': 0,
        'gold': 100
    }
    #
    test_quests = {
        'first_quest': {
            'quest_id': 'first_quest',
            'title': 'First Steps',
            'description': 'Complete your first quest',
         'reward_xp': 50,
            'reward_gold': 25,
            'required_level': 1,
            'prerequisite': 'NONE'
        }
    }
    #
    try:
        accept_quest(test_char, 'first_quest', test_quests)
        print("Quest accepted!")
    except QuestRequirementsNotMetError as e:
        print(f"Cannot accept: {e}")
