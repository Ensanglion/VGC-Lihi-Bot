import threading
import time
import pandas as pd
import re
import random
import pygetwindow as gw
from Classes import Mon, Field
from screenshot import capture_chat

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


def load_pokemon_names(csv_path="Pokemon_Data.csv"):
    try:
        dfMon = pd.read_csv(csv_path)
        return set(dfMon["Name"].str.strip())
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return set()

known_pokemon = load_pokemon_names()
print("Known Pokémon Names:", known_pokemon)  # Debugging

def load_pokemon_data(csv_path="Pokemon_Data.csv"):
    try:
        dfMon = pd.read_csv(csv_path)
        return dfMon
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame()

pokemon_data = load_pokemon_data()
print("Loaded Pokémon Data:", pokemon_data.head())  # Debugging

def extract_valid_name(full_name, bracket_name):
    full_name = full_name.strip()
    bracket_name = bracket_name.strip() if bracket_name else None
    
    if full_name in known_pokemon:
        return full_name
    elif bracket_name and bracket_name in known_pokemon:
        return bracket_name
    else:
        return None

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
        if move.name == "Hydro Steam" and field.weather in ["rain", "harsh sunlight"]:
            return 1.5
        if (field.weather == "rain" and move.type == "Water") or (field.weather == "harsh sunlight" and move.type == "Fire"):
            return 1.5
        if (field.weather == "rain" and move.type == "Fire") or (field.weather == "harsh sunlight" and move.type == "Water"):
            return 0.5
        
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
        if (field.terrain == "Electric" and move.type.lower() == "electric") or \
           (field.terrain == "Grassy" and move.type.lower() == "grass") or \
           (field.terrain == "Psychic" and move.type.lower() == "psychic"):
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
    if move.name == "Foul Play":
        A = target.Patk
    if move.name == "Body Press":
        A = attacker.Pdef
    D = target.Pdef if move.category == "physical" or move.name == "Psyshock" else target.SpD
    
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


dfMoves = pd.read_csv("Move_Data.csv")

field = Field()

perish_counters = {}

def stat_change_move(user, target, move, playerMons, oppMons):
    if move.name == "Swords Dance":
        user.modify_stats({"Patk": 2})
    elif move.name == "Nasty Plot":
        user.modify_stats({"SpA": 2})
    elif move.name == "Calm Mind":
        user.modify_stats({"SpA": 1, "SpD": 1})
    elif move.name == "Bulk Up":
        user.modify_stats({"Patk": 1, "Pdef": 1})
    elif move.name == "Dragon Dance":
        user.modify_stats({"Patk": 1, "Speed": 1})
    elif move.name == "Quiver Dance":
        user.modify_stats({"SpA": 1, "SpD": 1, "Speed": 1})
    elif move.name == "Haze":
        for team in [playerMons, oppMons]:
            for pokemon in team[:2]:
                pokemon.modify_stats({"Patk": 0, "Pdef": 0, "SpA": 0, "SpD": 0, "Speed": 0})
    elif move.name == "Parting Shot":
        target.modify_stats({"Patk": -1, "SpA": -1})
    elif move.name in ["Close Combat", "Armor Cannon", "Headlong Rush"]:
        user.modify_stats({"Pdef": -1, "SpD": -1})
    elif move.name in ["Draco Meteor", "Overheat", "Make It Rain"]:
        user.modify_stats({"SpA": -2})
    elif move.name in ["Meteor Beam", "Electro Shot"] and user.status != "Charging":
        user.modify_stats({"SpA": 1})
    elif move.name == "Breaking Swipe":
        for pokemon in oppMons[:2]:
            pokemon.modify_stats({"Patk": -1})
    elif move.name in ["Snarl", "Struggle Bug"]:
        for pokemon in oppMons[:2]:
            pokemon.modify_stats({"SpA": -1})
    elif move.name == "Play Rough":
        target.modify_stats({"Patk": -1})
    elif move.name == "Crunch":
        target.modify_stats({"SpD": -1})
    elif move.name in ["Moonblast", "Spirit Break"]:
        target.modify_stats({"SpA": -1})
    elif move.name in ["Bug Buzz", "Earth Power", "Flash Cannon", "Luster Purge", "Psychic", "Shadow Ball"]:
        target.modify_stats({"SpD": -1})
    elif move.name in ["Bleakwind Storm", "Electroweb", "Icy Wind"]:
        for pokemon in oppMons[:2]:
            pokemon.modify_stats({"Speed": -1})
    elif move.name == "Scale Shot":
        user.modify_stats({"Speed": 1, "Pdef": -1})
    elif move.name == "Coaching":
        target.modify_stats({"Patk": 1, "Pdef": 1})
    elif move.name == "Iron Defense":
        user.modify_stats({"Pdef": 2})
    elif move.name == "Fiery Dance":
        user.modify_stats({"SpA": 1})
    elif move.name == "Flame Charge":
        user.modify_stats({"Speed": 1})
    
def status_condition_move(user, target, move, oppMove, playerMons, oppMons):
    if move.name == "Burning Bulwark" and oppMove.category == "physical":
        target.status = "Burn"
    elif move.name in ["Will-O-Wisp", "Flametthrower", "Flare Blitz", "Sacred Fire"]:
        target.status = "Burn"
    elif move.name in ["Sandsear Storm", "Heat Wave"]:
        for pokemon in oppMons[:2]:
            pokemon.status = "Burn"
    elif move.name == "Blizzard":
        for pokemon in oppMons[:2]:
            pokemon.status = "Freeze"
    elif move.name in ["Freeze-Dry", "Ice Beam"]:
        target.status = "Freeze"
    elif move.name in ["Discharge", "Wildbolt Storm"]:
        for pokemon in oppMons[:2]:
            pokemon.status = "Paralysis"
    elif move.name in ["Thunder", "Thunder Wave", "Thunderbolt"]:
        target.status = "Paralysis"
    elif move.name == "Sludge Bomb":
        target.status = "Poison"
    elif move.name in ["Sleep Powder", "Spore"]:
        target.status = "Sleep"
    elif move.name == "Yawn":
        target.status = "Drowsy"
    elif move.name == "Alluring Voice" and target.stats_raised():
        target.status = "Confusion"
    elif move.name == "Hurricane":
        for pokemon in oppMons[:2]:
            pokemon.status = "Confusion"
    elif move.name == "Strange Steam":
        target.status = "Confusion"
    elif move.name == "Outrage":
        user.status = "Confusion"
    elif move.name in ["Air Slash", "Dark Pulse", "Fake Out", "Icicle Crash", "Iron Head"]:
        target.status = "Flinch"
    elif move.name == "Rock Slide":
        for pokemon in oppMons[:2]:
            pokemon.status = "Flinch"
    
    
    
def switch_out_move(user, target, move, playerMons, oppMons):
    if playerMons[2] is not None and playerMons[2].status != "Fainted" and playerMons[3] is not None and playerMons[3].status != "Fainted":
        if move.name in ["U-turn", "Volt Switch", "Parting Shot"]:
            temp = user
            user = playerMons[2]
            playerMons[2] = temp

def recoil_move(user, target, move, oppMove, playerMons, oppMons, field):
    if move.name in ["Struggle", "Substitute"]:
        user.take_damage(1/4*user.HP)
    elif move.name in ["Flare Blitz", "Wave Crash", "Wood Hammer"]:
        user.take_damage(1/3*(calculate_damage(user, target, move, field).mean()))
    elif move.name == "Wild Charge":
        user.take_damage(1/4*(calculate_damage(user, target, move, field).mean()))

def healing_move(user, target, move, playerMons, oppMons):
    if move.name == "Life Dew":
        for pokemon in playerMons[:2]:
            pokemon.currentHP += 1/4*pokemon.HP
    elif move.name == "Pollen Puff":
        if target in playerMons[:2]:
            target.currentHP += 1/2*(calculate_damage(user, target, move, field).mean())
    elif move.name == "Drain Punch" or "Horn Leech" or "Giga Drain" or "Draining Kiss" or "Parabolic Charge":
        target.currentHP += 1/2*(calculate_damage(user, target, move, field).mean())

def field_effect_move(user, target, move, field, playerMons, oppMons):
    if move.name == "Electric Terrain":
        field.terrain = "Electric"
    elif move.name == "Grassy Terrain":
        field.terrain = "Grassy"
    elif move.name == "Misty Terrain":
        field.terrain = "Misty"
    elif move.name == "Psychic Terrain":
        field.terrain = "Psychic"
    elif move.name in ["Ice Spinner", "Steel Roller"]:
        field.terrain = None
    elif move.name == "Sunny Day":
        field.weather = "Harsh sunlight"
    elif move.name == "Rain Dance":
        field.weather = "Rain"
    elif move.name == "Trick Room":
        field.TrickRoom = True
    if user in playerMons[:2]:
        if move.name == "Tailwind":
            field.playerTailwind = True
        elif move.name == "Reflect":
            field.playerReflect = True
        elif move.name == "Light Screen":
            field.playerLightScreen = True
        elif move.name == "Aurora Veil":
            field.playerReflect = True
            field.playerLightScreen = True
    elif user in oppMons[:2]:
        if move.name == "Tailwind":
            field.oppTailwind = True
        elif move.name == "Reflect":
            field.oppReflect = True
        elif move.name == "Light Screen":
            field.oppLightScreen = True
        elif move.name == "Aurora Veil":
            field.oppReflect = True
            field.oppLightScreen = True
    

def multi_hit_move(user, target, move, field, playerMons, oppMons):
    if move.name == "Surging Strikes":
        for i in range(3):
            target.take_damage(calculate_damage(user, target, move, field).mean())
    elif move.name == "Tachyon Cutter":
        for i in range(2):
            target.take_damage(calculate_damage(user, target, move, field).mean())
    elif move.name == "Scale Shot":
        for i in range(3):
            target.take_damage(calculate_damage(user, target, move, field).mean())

def charge_move(user, target, move, field, playerMons, oppMons):
    if user.status != "Charging" or user.status != "Recharging":
        if move.name == "Hyper Beam":
            target.take_damage(calculate_damage(user, target, move, field).mean())
            user.status = "Recharging"
            return
        elif move.name == "Electro Shot" and field.weather != "Rain":
            user.status = "Charging"
            return
        elif move.name == "Meteor Beam":
            user.status = "Charging"
            return

    if user.status == "Charging":
        if move.name == "Electro Shot":
            target.take_damage(calculate_damage(user, target, move, field).mean())
            user.status = None
        elif move.name == "Meteor Beam":
            target.take_damage(calculate_damage(user, target, move, field).mean())
            user.status = None
    elif user.status == "Recharging":
        user.take_damage(0)
        user.status = None



def protection_move(user, target, move, oppMove, field, playerMons, oppMons):
    if move.name == "Burning Bulwark":
        user.status = "Protected"
    elif move.name == "Detect":
        user.status = "Protected"
    elif move.name == "Protect":
        user.status = "Protected"
    elif move.name == "Spiky Shield":
        user.status = "Protected"
        for pokemon in oppMons[:2]:
            if pokemon.Move.category == "physical":
                pokemon.take_damage(1/8*pokemon.HP)
    elif move.name == "Wide Guard" and oppMove.spread:
        for pokemon in playerMons[:2]:
            pokemon.status = "Protected"
    

def extra_effect_move(user, target, move, field, playerMons, oppMons):
    if move.name == "Knock Off" and target.item and target.item.removable:
        target.Item = None
    elif move.name == "Ivy Cudgel" and user.type2 != None:
        move.type = user.type2
    elif move.name == "Grassy Glide" and field.terrain == "Grassy":
        move.priority = 1
    elif move.name == "Sacred Sword":
        temp = target.Pdef
        target.Pdef = target.original_stats["Pdef"]
        target.take_damage(calculate_damage(user, target, move, field).mean())
        target.Pdef = temp
    elif move.name == "Facade" and user.status in ["Burn", "Paralysis", "Poison", "Toxic"]:
        move.BP *= 2
    elif move.name == "Last Respects":
        for mon in playerMons:
            if mon.status == "Fainted":
                move.BP += 50
    elif move.name == "Weather Ball":
        if field.weather == "Harsh sunlight":
            move.type = "Fire"
        elif field.weather == "Rain":
            move.type = "Water"
        elif field.weather == "Snow":
            move.type = "Ice"
    if user.IsTera:
        if move.name == "Tera Blast":
            move.type = user.teraType
        elif move.name == "Tera Starstorm":
            move.type = "Stellar"
            move.spread = True
            if target.IsTera:
                target.take_damage(2*calculate_damage(user, target, move, field).mean())
    if move.name == "Expanding Force" and field.terrain == "Psychic":
        move.spread = True
    if move.name in ["Water Spout", "Erpution"]:
        move.BP = 150*user.currentHP/user.HP
    if move.name == "Ruination":
        target.currentHP = 1/2*target.currentHP
    if move.name in ["Fissure", "Sheer Cold"]:
        target.currentHP = 0
    if move.name in ["Thunder", "Bleakwind Strom", "Hurricane", "wildbolt Storm", "Sandsear Storm"] and field.weather == "Rain":
        move.accuracy = 100
    if move.name == "Blizzard" and field.weather == "Snow":
        move.accuracy = 100
    if move.name == "Final Gambit":
        target.take_damage(user.currentHP)
        user.currentHP = 0
    if move.name == "Rising Voltage" and field.terrain == "Electric":
        move.BP *= 2
    if move.name == "Trick":
        temp = user.Item
        user.Item = target.Item
        target.Item = temp
    if move.name == "Perish Song":
        for mon in playerMons[:2] + oppMons[:2]:  # Only affect the first two Pokémon in each team
            perish_counters[mon.name] = 3  # Set perish counter to 3 for each affected Pokémon
    
    # Decrement perish counters for all affected Pokémon
    for mon in playerMons[:2] + oppMons[:2]:  # Only affect the first two Pokémon in each team
        if mon.name in perish_counters:
            perish_counters[mon.name] -= 1  # Decrement perish counter
            if perish_counters[mon.name] == 0:
                mon.currentHP = 0  # Set HP to 0 if perish counter reaches 0


def apply_effects(user, move, target, field, targetMove, playerMons, oppMons):
    stat_change_move(user, target, move, playerMons, oppMons)
    status_condition_move(user, target, move, targetMove, playerMons, oppMons)
    switch_out_move(user, target, move, playerMons, oppMons)
    recoil_move(user, target, move, targetMove, playerMons, oppMons, field)
    healing_move(user, target, move, playerMons, oppMons)
    field_effect_move(user, target, move, field)
    multi_hit_move(user, target, move, field, playerMons, oppMons)
    charge_move(user, target, move, field, playerMons, oppMons)
    protection_move(user, target, move, field, playerMons, oppMons)
    extra_effect_move(user, target, move, field, playerMons, oppMons)



def parse_battle_text(battle_text, field, known_pokemon):
    print("Debug - Captured Battle Text:", battle_text)  # Debugging

    go_pattern = re.compile(r'Go!\s*([\w\s-]+?)(?:\s*\(([\w\s-]+)\))?', re.IGNORECASE)
    sent_out_pattern = re.compile(r'sent out\s*([\w\s-]+?)(?:\s*\(([\w\s-]+)\))?', re.IGNORECASE)
    move_pattern = re.compile(r'([\w\s-]+) used ([\w\s-]+)!', re.IGNORECASE)
    opposing_move_pattern = re.compile(r'Opposing ([\w\s-]+) used ([\w\s-]+)!', re.IGNORECASE)

    print("Regex Matches for Go Pattern:", go_pattern.findall(battle_text))  # Debugging
    print("Regex Matches for Sent Out Pattern:", sent_out_pattern.findall(battle_text))  # Debugging

    for match in go_pattern.findall(battle_text):
        nickname, chosen_name = match
        valid_name = extract_valid_name(chosen_name, nickname)

        if valid_name:
            pokemon_row = pokemon_data[pokemon_data["Name"].str.strip() == valid_name]
            if not pokemon_row.empty:
                row = pokemon_row.iloc[0]
                if not any(mon.name == row["Name"] for mon in field.playerMons):
                    new_mon = Mon(
                        name=row["Name"], type1=row["Type1"], type2=row["Type2"],
                        HP=row["HP"], Patk=row["Attack"], Pdef=row["Defense"],
                        SpA=row["Special Attack"], SpD=row["Special Defense"], Speed=row["Speed"],
                        moves=[], ability=row["Ability"]
                    )
                    field.playerMons.append(new_mon)
                    print(f"Added player Pokémon: {nickname} ({row['Name']})")
    
    for match in sent_out_pattern.findall(battle_text):
        nickname, chosen_name = match
        valid_name = extract_valid_name(chosen_name, nickname)

        if valid_name:
            pokemon_row = pokemon_data[pokemon_data["Name"].str.strip() == valid_name]
            if not pokemon_row.empty:
                row = pokemon_row.iloc[0]
                if not any(mon.name == row["Name"] for mon in field.oppMons):
                    new_mon = Mon(
                        name=row["Name"], type1=row["Type1"], type2=row["Type2"],
                        HP=row["HP"], Patk=row["Attack"], Pdef=row["Defense"],
                        SpA=row["Special Attack"], SpD=row["Special Defense"], Speed=row["Speed"],
                        moves=[], ability=row["Ability"]
                    )
                    field.oppMons.append(new_mon)
                    print(f"Added opponent Pokémon: {nickname} ({row['Name']})")
    
    print("Player Pokémon List after parsing:", [mon.name for mon in field.playerMons])  # Debugging
    print("Opponent Pokémon List after parsing:", [mon.name for mon in field.oppMons])  # Debugging

def monitor_battle(field, known_pokemon):
    while any("Showdown!" in w.title for w in gw.getWindowsWithTitle("Showdown!")):
        battle_text = capture_chat()
        print("Captured Battle Text:", battle_text)  # Debugging
        if battle_text:
            parse_battle_text(battle_text, field, known_pokemon)
        time.sleep(2)

try:
    field = Field()
    monitor_battle(field, known_pokemon)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    print("Final Player's Pokémon:", [mon.name for mon in field.playerMons])
    print("Final Opponent's Pokémon:", [mon.name for mon in field.oppMons])
