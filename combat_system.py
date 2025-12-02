"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Xavier Rothwell
AI Usage: chat gpt was used to help with the formating and debugging of the code

Handles combat mechanics
"""
import random
from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================


def create_enemy(enemy_type):
    enemy_type = enemy_type.lower()  # make input flexible

    enemy_stats = {
        "goblin": {
            "name": "Goblin",
            "health": 50,
            "max_health": 50,
            "strength": 8,
            "magic": 2,
            "xp_reward": 25,
            "gold_reward": 10
        },
        "orc": {
            "name": "Orc",
            "health": 80,
            "max_health": 80,
            "strength": 12,
            "magic": 5,
            "xp_reward": 50,
            "gold_reward": 25
        },
        "dragon": {
            "name": "Dragon",
            "health": 200,
            "max_health": 200,
            "strength": 25,
            "magic": 15,
            "xp_reward": 200,
            "gold_reward": 100
        }
    }

    if enemy_type not in enemy_stats:
        raise InvalidTargetException(f"Unknown enemy type: {enemy_type}")

    return enemy_stats[enemy_type].copy()
    pass

def get_random_enemy_for_level(character_level):

    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")
    pass


# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        self.character = character
        self.enemy = enemy

        self.combat_active = True
        
        self.turn = 1
        pass
    
    def start_battle(self):

        if self.character["health"] <= 0:
            raise CharacterDeadException("Character is dead and cannot fight.")

        # loop while both sides are alive and combat is active
        while self.combat_active:

            # PLAYER TURN
            self.player_turn()
            winner = self.check_battle_end()
            if winner is not None:
                break

            # ENEMY TURN
            self.enemy_turn()
            winner = self.check_battle_end()
            if winner is not None:
                break

        # next round
        self.turn += 1

        # after battle ends, build result dictionary
        if winner == "player":
            rewards = get_victory_rewards(self.enemy)
            return {
                "winner": "player",
                "xp_gained": rewards["xp"],
                "gold_gained": rewards["gold"],
            }

        else:
            return {
                "winner": "enemy",
                "xp_gained": 0,
                "gold_gained": 0,
            }
        pass
    
    def player_turn(self):

        if not self.combat_active:
            raise CombatNotActiveException("Combat is not active.")
        
        damage = self.calculate_damage(self.character, self.enemy)
        self.apply_damage(self.enemy, damage)

        display_battle_log(f"You attack the {self.enemy['name']} for {damage} damage!")
        pass
    
    def enemy_turn(self):

        if not self.combat_active:
            raise CombatNotActiveException("Combat is not active.")

        # enemy always does a basic attack
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)

        display_battle_log(f"The {self.enemy['name']} attacks you for {damage} damage!")
        pass
    
    def calculate_damage(self, attacker, defender):

        damage = attacker["strength"] - (defender["strength"] // 4)

        # damage can never be lower than 1
        if damage < 1:
            damage = 1

        return damage
        pass
    
    def apply_damage(self, target, damage):

        target["health"] -= damage

        # health should not go below 0
        if target["health"] < 0:
            target["health"] = 0
        pass
    
    def check_battle_end(self):

        if self.enemy["health"] <= 0:
            self.combat_active = False
            return "player"

        # player dead, enemy wins
        if self.character["health"] <= 0:
            self.combat_active = False
            return "enemy"

        return None
        pass
    
    def attempt_escape(self):

        roll = random.random()  # random number 0 to 1

        if roll < 0.5:
            # success
            self.combat_active = False
            display_battle_log("You escaped successfully!")
            return True
        else:
            # fail
            display_battle_log("You failed to escape!")
            return False
        pass


# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):

    char_class = character["class"]

    if char_class == "Warrior":
        return warrior_power_strike(character, enemy)

    elif char_class == "Mage":
        return mage_fireball(character, enemy)

    elif char_class == "Rogue":
        return rogue_critical_strike(character, enemy)

    elif char_class == "Cleric":
        return cleric_heal(character)

    else:
        raise InvalidTargetException("Unknown character class.")
    pass


def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    base = character["strength"] * 2

    if base < 1:
        damage = 1
    else:
        damage = base

    enemy["health"] -= damage

    if enemy["health"] < 0:
        enemy["health"] = 0

    return f"Warrior uses Power Strike for {damage} damage!"
    pass


def mage_fireball(character, enemy):
    """Mage special ability"""
    base = character["magic"] * 2

    if base < 1:
        damage = 1
    else:
        damage = base

    enemy["health"] -= damage

    if enemy["health"] < 0:
        enemy["health"] = 0

    return f"Mage casts Fireball for {damage} damage!"
    pass


def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    crit = random.random() < 0.5

    if crit:
        base = character["strength"] * 3
        message = "Critical hit!"
    else:
        base = character["strength"]
        message = "Regular hit."

    if base < 1:
        damage = 1
    else:
        damage = base

    enemy["health"] -= damage

    if enemy["health"] < 0:
        enemy["health"] = 0

    return f"Rogue uses Critical Strike: {message} {damage} damage!"
    pass


def cleric_heal(character):
    """Cleric special ability"""
    character["health"] += 30

    if character["health"] > character["max_health"]:
        character["health"] = character["max_health"]

    return "Cleric casts Heal and restores 30 HP"
    pass


# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    # TODO: Implement fight check
    pass


def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    Returns: Dictionary with 'xp' and 'gold'
    """
    return {
        "xp": enemy["xp_reward"],
        "gold": enemy["gold_reward"]
    }
    pass


def display_combat_stats(character, enemy):
    """
    Display current combat status
    Shows both character and enemy health/stats
    """
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    pass


def display_battle_log(message):
    """
    Display a formatted battle message
    """
    print(f">>> {message}")
    pass
# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
     Test enemy creation
     try:
         goblin = create_enemy("goblin")
         print(f"Created {goblin['name']}")
     except InvalidTargetError as e:
         print(f"Invalid enemy: {e}")
    
     Test battle
     test_char = {
         'name': 'Hero',
         'class': 'Warrior',
         'health': 120,
         'max_health': 120,
         'strength': 15,
         'magic': 5
     }
    
     battle = SimpleBattle(test_char, goblin)
     try:
         result = battle.start_battle()
         print(f"Battle result: {result}")
     except CharacterDeadError:
         print("Character is dead!")

