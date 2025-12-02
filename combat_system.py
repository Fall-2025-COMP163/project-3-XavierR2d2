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
    enemy_type = enemy_type.lower()

    enemies = {
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

    if enemy_type not in enemies:
        raise InvalidTargetError(f"unknown enemy type: {enemy_type}")

    return enemies[enemy_type].copy()


def get_random_enemy_for_level(character_level):
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")


# ---------------------------------------------------------
# COMBAT SYSTEM         
# ---------------------------------------------------------

class SimpleBattle:
    def __init__(self, character, enemy):
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn = 1

    def start_battle(self):
        if self.character["health"] <= 0:
            raise CharacterDeadError("character is already dead")

        winner = None

        while self.combat_active:
            # player turn
            self.player_turn()
            winner = self.check_battle_end()
            if winner:
                break

            # enemy turn
            self.enemy_turn()
            winner = self.check_battle_end()
            if winner:
                break

            self.turn += 1

        # build result packet
        if winner == "player":
            rewards = get_victory_rewards(self.enemy)
            return {
                "winner": "player",
                "xp_gained": rewards["xp"],
                "gold_gained": rewards["gold"]
            }
        else:
            return {
                "winner": "enemy",
                "xp_gained": 0,
                "gold_gained": 0
            }

    def player_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError("combat is not active")

        damage = self.calculate_damage(self.character, self.enemy)
        self.apply_damage(self.enemy, damage)
        display_battle_log(f"you hit the {self.enemy['name']} for {damage}")

    def enemy_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError("combat is not active")

        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"the {self.enemy['name']} hits you for {damage}")

    def calculate_damage(self, attacker, defender):
        dmg = attacker["strength"] - (defender["strength"] // 4)
        if dmg < 1:
            dmg = 1
        return dmg

    def apply_damage(self, target, damage):
        target["health"] -= damage
        if target["health"] < 0:
            target["health"] = 0

    def check_battle_end(self):
        if self.enemy["health"] <= 0:
            self.combat_active = False
            return "player"
        if self.character["health"] <= 0:
            self.combat_active = False
            return "enemy"
        return None

    def attempt_escape(self):
        roll = random.random()
        if roll < 0.5:
            self.combat_active = False
            display_battle_log("you escaped successfully")
            return True
        else:
            display_battle_log("escape failed")
            return False


# ---------------------------------------------------------
# SPECIAL ABILITIES    
# ---------------------------------------------------------

def use_special_ability(character, enemy):
    c = character["class"]

    if c == "Warrior":
        return warrior_power_strike(character, enemy)
    elif c == "Mage":
        return mage_fireball(character, enemy)
    elif c == "Rogue":
        return rogue_critical_strike(character, enemy)
    elif c == "Cleric":
        return cleric_heal(character)
    else:
        raise InvalidTargetError("unknown class")

def warrior_power_strike(character, enemy):
    dmg = max(1, character["strength"] * 2)
    enemy["health"] -= dmg
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"warrior uses power strike for {dmg}"

def mage_fireball(character, enemy):
    dmg = max(1, character["magic"] * 2)
    enemy["health"] -= dmg
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"mage casts fireball for {dmg}"

def rogue_critical_strike(character, enemy):
    crit = random.random() < 0.5
    if crit:
        dmg = max(1, character["strength"] * 3)
        note = "critical hit"
    else:
        dmg = max(1, character["strength"])
        note = "normal hit"

    enemy["health"] -= dmg
    if enemy["health"] < 0:
        enemy["health"] = 0

    return f"rogue critical strike: {note}, {dmg} damage"

def cleric_heal(character):
    character["health"] += 30
    if character["health"] > character["max_health"]:
        character["health"] = character["max_health"]
    return "cleric heals for 30"


# ---------------------------------------------------------
# COMBAT UTILITIES
# ---------------------------------------------------------

def can_character_fight(character):
    # character must have hp above zero
    return character["health"] > 0

def get_victory_rewards(enemy):
    return {
        "xp": enemy["xp_reward"],
        "gold": enemy["gold_reward"]
    }

def display_combat_stats(character, enemy):
    print(f"\n{character['name']}: {character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: {enemy['health']}/{enemy['max_health']}")

def display_battle_log(message):
    print(f">>> {message}")

