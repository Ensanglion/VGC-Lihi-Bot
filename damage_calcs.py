from Classes import Mon, Field, Item, Move
import random

type_chart = {
    'Normal': {
        'Normal': 1, 'Fire': 1, 'Water': 1, 'Grass': 1, 'Electric': 1, 'Ice': 1, 'Fighting': 1, 'Poison': 1, 'Ground': 1,
        'Flying': 1, 'Psychic': 1, 'Bug': 1, 'Rock': 0.5, 'Ghost': 0, 'Dragon': 1, 'Dark': 1, 'Steel': 0.5,  'Fairy': 1
    },
    'Fire': {
        'Normal': 1, 'Fire': 0.5, 'Water': 0.5, 'Grass': 2, 'Electric': 1, 'Ice': 2, 'Fighting': 1, 'Poison': 1, 'Ground': 1, 
        'Flying': 1, 'Psychic': 1, 'Bug': 2, 'Rock': 0.5, 'Ghost': 1, 'Dragon': 0.5, 'Dark': 1, 'Steel': 2, 'Fairy': 1
    },
    'Water': {
        'Normal': 1, 'Fire': 2, 'Water': 0.5, 'Grass': 0.5, 'Electric': 1, 'Ice': 1, 'Fighting': 1, 'Poison': 1, 'Ground': 2, 
        'Flying': 1, 'Psychic': 1, 'Bug': 1, 'Rock': 2, 'Ghost': 1, 'Dragon': 0.5, 'Dark': 1, 'Steel': 1, 'Fairy': 1
    },
    'Grass': {
        'Normal': 1, 'Fire': 0.5, 'Water': 2, 'Grass': 0.5, 'Electric': 1, 'Ice': 1, 'Fighting': 1, 'Poison': 0.5, 'Ground': 2,
        'Flying': 0.5, 'Psychic': 1, 'Bug': 0.5, 'Rock': 2, 'Ghost': 1, 'Dragon': 0.5, 'Dark': 1, 'Steel': 0.5, 'Fairy': 1
    },
    'Electric': {
        'Normal': 1, 'Fire': 1, 'Water': 2, 'Grass': 0.5, 'Electric': 0.5, 'Ice': 1, 'Fighting': 1, 'Poison': 1, 'Ground': 0,
        'Flying': 2, 'Psychic': 1, 'Bug': 1, 'Rock': 1, 'Ghost': 1, 'Dragon': 0.5, 'Dark': 1, 'Steel': 1, 'Fairy': 1
    },
    'Ice': {
        'Normal': 1, 'Fire': 0.5, 'Water': 0.5, 'Grass': 2, 'Electric': 1, 'Ice': 0.5, 'Fighting': 1, 'Poison': 1, 'Ground': 2,
        'Flying': 2, 'Psychic': 1, 'Bug': 1, 'Rock': 1, 'Ghost': 1, 'Dragon': 2, 'Dark': 1, 'Steel': 0.5, 'Fairy': 1
    },
    'Fighting': {
        'Normal': 2, 'Fire': 1, 'Grass': 1, 'Water': 1, 'Electric': 1, 'Ice': 2, 'Fighting': 1, 'Poison': 0.5, 'Ground': 1,
        'Flying': 0.5, 'Psychic': 0.5, 'Bug': 0.5, 'Rock': 2, 'Ghost': 0, 'Dragon': 1, 'Dark': 2, 'Steel': 2, 'Fairy': 2
    },
    'Poison': {
        'Normal': 1, 'Fire': 1, 'Water': 1, 'Grass': 2, 'Electric': 1, 'Ice': 1, 'Fighting': 1, 'Poison': 0.5, 'Ground': 0.5,
        'Flying': 1, 'Psychic': 2, 'Bug': 1, 'Rock': 0.5, 'Ghost': 1, 'Dragon': 1, 'Dark': 1, 'Steel': 0, 'Fairy': 0.5
    },
    'Ground': {
        'Normal': 1, 'Fire': 2, 'Water': 1, 'Grass': 0.5, 'Electric': 2, 'Ice': 1, 'Fighting': 1, 'Poison': 2, 'Ground': 1,
        'Flying': 0, 'Psychic': 1, 'Bug': 0.5, 'Rock': 2, 'Ghost': 1, 'Dragon': 1, 'Dark': 1, 'Steel': 2, 'Fairy': 1
    },
    'Flying': {
        'Normal': 1, 'Fire': 1, 'Water': 1, 'Grass': 2, 'Electric': 0.5, 'Ice': 1, 'Fighting': 2, 'Poison': 1, 'Ground': 1,
        'Flying': 1, 'Psychic': 1, 'Bug': 2, 'Rock': 0.5, 'Ghost': 1, 'Dragon': 1, 'Dark': 1, 'Steel': 0.5, 'Fairy': 1
    },
    'Psychic': {
        'Normal': 1, 'Fire': 1, 'Water': 1, 'Grass': 1, 'Electric': 1, 'Ice': 1, 'Fighting': 2, 'Poison': 2, 'Ground': 1,
        'Flying': 1, 'Psychic': 0.5, 'Bug': 1, 'Rock': 1, 'Ghost': 1, 'Dragon': 1, 'Dark': 0, 'Steel': 0.5, 'Fairy': 1
    },
    'Bug': {
        'Normal': 1, 'Fire': 0.5, 'Water': 1, 'Grass': 2, 'Electric': 1, 'Ice': 1, 'Fighting': 0.5, 'Poison': 0.5, 'Ground': 1,
        'Flying': 0.5, 'Psychic': 2, 'Bug': 1, 'Rock': 1, 'Ghost': 0.5, 'Dragon': 1, 'Dark': 2, 'Steel': 0.5, 'Fairy': 0.5
    },
    'Rock': {
        'Normal': 1, 'Fire': 2, 'Water': 1, 'Grass': 1, 'Electric': 1, 'Ice': 2, 'Fighting': 0.5, 'Poison': 1, 'Ground': 0.5,
        'Flying': 2, 'Psychic': 1, 'Bug': 2, 'Rock': 1, 'Ghost': 1, 'Dragon': 1, 'Dark': 1, 'Steel': 2, 'Fairy': 1
    },
    'Ghost': {
        'Normal': 0, 'Fire': 1, 'Water': 1, 'Grass': 1, 'Electric': 1, 'Ice': 1, 'Fighting': 1, 'Poison': 1, 'Ground': 1,
        'Flying': 1, 'Psychic': 1, 'Bug': 1, 'Rock': 1, 'Ghost': 2, 'Dragon': 1, 'Dark': 2, 'Steel': 1, 'Fairy': 1
    },
    'Dragon': {
        'Normal': 1, 'Fire': 1, 'Water': 1, 'Grass': 1, 'Electric': 1, 'Ice': 1, 'Fighting': 1, 'Poison': 1, 'Ground': 1,
        'Flying': 1, 'Psychic': 1, 'Bug': 1, 'Rock': 1, 'Ghost': 1, 'Dragon': 2, 'Dark': 1, 'Steel': 0.5, 'Fairy': 0
    },
    'Dark': {
        'Normal': 1, 'Fire': 1, 'Water': 1, 'Grass': 1, 'Electric': 1, 'Ice': 1, 'Fighting': 0.5, 'Poison': 1, 'Ground': 1,
        'Flying': 1, 'Psychic': 2, 'Bug': 1, 'Rock': 1, 'Ghost': 2, 'Dragon': 1, 'Dark': 0.5, 'Steel': 1, 'Fairy': 0.5
    },
    'Steel': {
        'Normal': 1, 'Fire': 0.5, 'Water': 0.5, 'Grass': 1, 'Electric': 0.5, 'Ice': 2, 'Fighting': 1, 'Poison': 1, 'Ground': 1,
        'Flying': 1, 'Psychic': 1, 'Bug': 1, 'Rock': 2, 'Ghost': 1, 'Dragon': 1, 'Dark': 1, 'Steel': 0.5, 'Fairy': 2
    },
    'Fairy': {
        'Normal': 1, 'Fire': 0.5, 'Water': 1, 'Grass': 1, 'Electric': 1, 'Ice': 1, 'Fighting': 2, 'Poison': 2, 'Ground': 1,
        'Flying': 1, 'Psychic': 1, 'Bug': 1, 'Rock': 1, 'Ghost': 1, 'Dragon': 2, 'Dark': 2, 'Steel': 0.5, 'Fairy': 1
    }
}

stat_changes = {
    -6: 0.25,
    -5: 0.28,
    -4: 0.33,
    -3: 0.4,
    -2: 0.5,
    -1: 0.66,
    0: 1,
    1: 1.5,
    2: 2,
    3: 2.5,
    4: 3,
    5: 3.5,
    6: 4
}


class DamageCalculator:
    @staticmethod
    def target_multiplier(move, field):
        """Returns the target multiplier (1 or 0.75)."""
        if move.spread:
            opponents = [field.oppLeft, field.oppRight]
            num_targets = sum(1 for mon in opponents if mon is not None)
            return 0.75 if num_targets > 1 else 1
        return 1
    
    @staticmethod
    def weather_multiplier(move, user, field):
        """Returns the weather multiplier (1 or 1.5)."""
        if any(mon and mon.ability in ["Cloud Nine", "Air Lock"] for mon in [field.playerLeft, field.playerRight, field.oppLeft, field.oppRight]):
            return 1
        if (field.weather == "rain" and move.type == "Water") or (field.weather == "harsh sunlight" and move.type == "Fire"):
            return 1.5
        return 1
    
    @staticmethod
    def stab_multiplier(move, user):
        """Returns the STAB multiplier (1, 1.5, 2, or 2.25)."""
        base_stab = 1.5 if move.type in [user.type1, user.type2] else 1
        if user.IsTera:
            if user.teraType in [user.type1, user.type2]:
                base_stab = 2 if move.type in [user.type1, user.type2] else 1.5
        if user.ability == "Adaptability":
            base_stab *= 1.5
        return base_stab
    
    @staticmethod
    def type_multiplier(move, user, target):
        """Returns the type effectiveness multiplier with special cases."""
        effectiveness = type_chart[move.type][target.type1] * type_chart[move.type][target.type2]
        
        if move.type == "Ground" and "Flying" in [target.type1, target.type2] and target.item == "Iron Ball":
            effectiveness = 1
        if move.type in ["Normal", "Fighting"] and "Ghost" in [target.type1, target.type2] and user.ability in ["Scrappy", "Mind's Eye"]:
            effectiveness = 1
        if move.name == "Freeze-Dry" and "Water" in [target.type1, target.type2]:
            effectiveness *= 2
        return effectiveness
    
    @staticmethod
    def burn_multiplier(user, move):
        """Returns the burn multiplier (0.5 or 1)."""
        if user.status == "burned" and user.ability != "Guts" and move.category == "Physical":
            return 0.5
        return 1
    
    @staticmethod
    def other_effects_multiplier(move, user, target, field):
        """Returns the multiplier for all other special effects."""
        multiplier = 1
        
        if user.ability == "Guts" and user.status in ["burned", "paralyzed", "poisoned"]:
            multiplier *= 2
        if move.name == "Brine" and target.currentHP < (target.HP / 2):
            multiplier *= 2
        if move.name in ["Venoshock", "Barb Barrage"] and target.status == "poisoned":
            multiplier *= 2
        if move.name in ["Solar Beam", "Solar Blade"] and field.weather in ["rain", "sandstorm", "snow"]:
            multiplier *= 0.5
        if move.name == "Knock Off" and target.item and target.item.removable:
            multiplier *= 1.5
        if move.name == "Expanding Force" and field.terrain == "Psychic":
            multiplier *= 1.5
        if field.terrain == "Grassy" and move.name == "Earthquake":
            multiplier *= 0.5
        if field.terrain == "Misty" and move.type == "Dragon":
            multiplier *= 0.5
        if field.terrain in ["Grassy", "Electric", "Psychic"] and move.type.lower() in field.terrain.lower():
            multiplier *= 5325 / 4096
        if user.ability == "Supreme Overlord":
            multiplier *= 1 + (0.1 * min(5, user.fainted_ally_count))
        if user.ability in ["Aerilate", "Pixilate", "Refrigerate", "Galvanize"] and move.type == "Normal":
            multiplier *= 4915 / 4096
        if user.ability == "Analytic" and target.speed > user.speed:
            multiplier *= 5325 / 4096
        if user.ability == "Sand Force" and field.weather == "sandstorm" and move.type in ["Ground", "Rock", "Steel"]:
            multiplier *= 5325 / 4096
        if user.ability == "Technician" and move.BP <= 60:
            multiplier *= 1.5
        if (field.oppReflect and move.category == "Physical") or (field.oppLightScreen and move.category == "Special"):
            multiplier *= 0.5
        if move.name in ["Electro Drift", "Collision Course"] and DamageCalculator.type_multiplier(move, user, target) >= 2:
            multiplier *= 5461 / 4096
        if target.ability in ["Multiscale", "Shadow Shield"] and target.currentHP == target.HP:
            multiplier *= 0.5
        if target.ability == "Fluffy" and move.contact:
            multiplier *= 0.5
        if target.ability == "Fluffy" and move.type == "Fire":
            multiplier *= 2
        if target.ability == "Ice Scales" and move.category == "Special":
            multiplier *= 0.5
        if user.heldItem == "Life Orb":
            multiplier *= 5324 / 4096
        
        return multiplier



def calculate_damage(attacker, target, move, field):
    BP = move.BP
    A = attacker.Patk if move.category == "physical" else attacker.SpA
    D = target.Pdef if move.category == "physical" else target.SpD
    
    target_multiplier = DamageCalculator.target_multiplier(move, field)
    weather_multiplier = DamageCalculator.weather_multiplier(move, attacker, field)
    stab_multiplier = DamageCalculator.stab_multiplier(move, attacker)
    type_multiplier = DamageCalculator.type_multiplier(move, attacker, target)
    burn_multiplier = DamageCalculator.burn_multiplier(attacker, move)
    other_effects_multiplier = DamageCalculator.other_effects_multiplier(move, attacker, target, field)
    
    # Critical hit check
    if move.name in ["Storm Throw", "Frost Breath", "Zippy Zap", "Surging Strikes", "Wicked Blow", "Flower Trick"]:
        crit_multiplier = 1.5  # Always crit
    else:
        crit_multiplier = 1.5 if random.randint(1, 24) == 1 else 1  # 1/24 chance
    
    # Check for abilities that negate crits
    if target.ability in ["Battle Armor", "Shell Armor"]:
        crit_multiplier = 1  # No crit damage if these abilities are active
    
    damage_rolls = []

    for i in range(85, 101):
        
        damage = (((2 * 50 / 5 + 2) * BP * A / D) / 50 + 2)
        damage *= target_multiplier * weather_multiplier * stab_multiplier * type_multiplier
        damage *= burn_multiplier * other_effects_multiplier * (i / 100) * crit_multiplier
        damage_rolls.append(int(damage))
    
    return damage_rolls  # Return rounded damage as an integer
