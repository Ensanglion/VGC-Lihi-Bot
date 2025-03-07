import pandas as pd
from Classes import Mon, Field, Item, Move
import random
from game_logic import DamageCalculator, calculate_damage
import time
import math

# Load the CSV into a DataFrame
df = pd.read_csv("Pokemon_Data.csv")
# Standardize column names by stripping spaces and making them lowercase
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Rename columns to match Mon class attributes
df.rename(columns={
    "name": "name",
    "type1": "type1",
    "type2": "type2",
    "hp": "HP",
    "attack": "Patk",
    "defense": "Pdef",
    "special_attack": "SpA",
    "special_defense": "SpD",
    "speed": "Speed",
    "ability": "ability"
}, inplace=True)

mons = []

for _, row in df.iterrows():
    mon = Mon(
        name=row["name"],
        type1=row["type1"],
        type2=row["type2"],
        HP=row["HP"],
        Patk=row["Patk"],
        Pdef=row["Pdef"],
        SpA=row["SpA"],
        SpD=row["SpD"],
        Speed=row["Speed"],
        ability=row["ability"]
        # Moves, item, status, and teraType will be set manually later
    )
    mons.append(mon)

team_names = ["Miraidon", "Iron Bundle", "Incineroar", "Iron Hands", "Iron Treads", "Ogerpon Hearthflame"]
team = []
for mon_name in team_names:
    for mon in mons:
        if mon.name == mon_name:
            team.append(Mon(
        name=mon.name,
        type1=mon.type1,
        type2=mon.type2,
        HP=mon.HP,
        Patk=mon.Patk,
        Pdef=mon.Pdef,
        SpA=mon.SpA,
        SpD=mon.SpD,
        Speed=mon.Speed,
        move1="Discharge" if mon_name == "Miraidon" else
              "Icy Wind" if mon_name == "Iron Bundle" else
              "Fake Out" if mon_name in ["Incineroar", "Iron Hands"] else
              "Steel Roller" if mon_name == "Iron Treads" else
              "Ivy Cudgel",
        move2="Electro Drift" if mon_name == "Miraidon" else
              "Freeze-Dry" if mon_name == "Iron Bundle" else
              "Parting Shot" if mon_name == "Incineroar" else
              "Wild Charge" if mon_name == "Iron Hands" else
              "Rock Slide" if mon_name == "Iron Treads" else
              "Horn Leech",
        move3="Dazzling Gleam" if mon_name == "Miraidon" else
              "Hydro Pump" if mon_name == "Iron Bundle" else
              "Flare Blitz" if mon_name == "Incineroar" else
              "Drain Punch" if mon_name == "Iron Hands" else
              "High Horsepower" if mon_name == "Iron Treads" else
              "Follow Me",
        move4="Volt Switch" if mon_name == "Miraidon" else
              "Protect" if mon_name in ["Iron Bundle", "Iron Treads"] else
              "Knock Off" if mon_name == "Incineroar" else
              "Heavy Slam" if mon_name == "Iron Hands" else
              "Spiky Shield",
        heldItem="Choice Specs" if mon_name == "Miraidon" else
                 "Focus Sash" if mon_name == "Iron Bundle" else
                 "Safety Goggles" if mon_name == "Incineroar" else
                 "Assault Vest" if mon_name == "Iron Hands" else
                 "Life Orb" if mon_name == "Iron Treads" else
                 "Hearthflame Mask",
        ability=mon.ability,  # Keep the default ability from the dataset
        teraType="Electric" if mon_name == "Miraidon" else
                 "Ghost" if mon_name in ["Iron Bundle", "Incineroar"] else
                 "Fighting" if mon_name == "Iron Hands" else
                 "Ground" if mon_name == "Iron Treads" else
                 "Fire"
    ))



# Define Moves
dazzling_gleam = Move("Dazzling Gleam", BP=80, PP=10, type="Fairy", category="Special", contact=False, spread=True, priority=0)

# Define Pokémon
miraidon = team[0]
iron_hands = team[3]

# Define Field
test_field = Field(playerLeft=miraidon, oppLeft=iron_hands)

# Define Damage Calculator

damage = calculate_damage(miraidon, iron_hands, dazzling_gleam, test_field)
print(f"{team[0].name}'s {team[0].move3} deals {damage} damage to {team[3].name}.")

# Showdown sucks
print(f"Turns to KO at worst case: {math.ceil(iron_hands.currentHP / damage[0])}, \nat best case: {math.ceil(iron_hands.currentHP / damage[15])}")