"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

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
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
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
        raise InvalidTargetError(f"Unknown enemy type: {enemy_type}")

    return enemy_stats[enemy_type].copy()
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward
    pass

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    pass

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        self.character = character
        self.enemy = enemy

        self.combat_active = True
        
        self.turn = 1
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        pass
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        if self.character["health"] <= 0:
            raise CharacterDeadError("Character is dead and cannot fight.")

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
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        pass
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")
        
        damage = self.calculate_damage(self.character, self.enemy)
        self.apply_damage(self.enemy, damage)

        display_battle_log(f"You attack the {self.enemy['name']} for {damage} damage!")
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        pass
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")

        # enemy always does a basic attack
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)

        display_battle_log(f"The {self.enemy['name']} attacks you for {damage} damage!")
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        pass
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
         damage = attacker["strength"] - (defender["strength"] // 4)

    # damage can never be lower than 1
        if damage < 1:
            damage = 1

        return damage
        # TODO: Implement damage calculation
        pass
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        target["health"] -= damage

        # health should not go below 0
        if target["health"] < 0:
            target["health"] = 0
        # TODO: Implement damage application
        pass
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        if self.enemy["health"] <= 0:
            self.combat_active = False
            return "player"

    # player dead, enemy wins
        if self.character["health"] <= 0:
            self.combat_active = False
            return "enemy"

        return None
        # TODO: Implement battle end check
        pass
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
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
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        pass

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
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
        raise InvalidTargetError("Unknown character class.")
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
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
    # TODO: Implement power strike
    # Double strength damage
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
    # TODO: Implement fireball
    # Double magic damage
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
    # TODO: Implement critical strike
    # 50% chance for triple damage
    pass

def cleric_heal(character):
    """Cleric special ability"""
    character["health"] += 30

    if character["health"] > character["max_health"]:
        character["health"] = character["max_health"]

    return "Cleric casts Heal and restores 30 HP"
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    pass

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
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
    # TODO: Implement reward calculation
    pass

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    pass

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
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

