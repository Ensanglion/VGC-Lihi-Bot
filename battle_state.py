import threading
import time
import pandas as pd
import re
import pygetwindow as gw
from Classes import Mon, Field
from screenshot import capture_chat

def load_pokemon_names(csv_path="Pokemon_Data.csv"):
    try:
        df = pd.read_csv(csv_path)
        return set(df["Name"].str.strip())
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return set()

known_pokemon = load_pokemon_names()

def load_pokemon_data(csv_path="Pokemon_Data.csv"):
    """Load Pokémon data from a CSV file into a DataFrame."""
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

# Load the Pokémon data into a DataFrame
pokemon_data = load_pokemon_data()

def parse_battle_text(battle_text, field, known_pokemon):
    print("Debug - Captured Battle Text:")  # Debug output
    print(battle_text)  # Print the captured text for debugging

    # Updated regex patterns to capture full names correctly
    go_pattern = re.compile(r'Go!\s*([\w\s-]+)(?:\s*!\s*\(([^)]+)\))?', re.IGNORECASE)
    sent_out_pattern = re.compile(r'sent out\s*([\w\s-]+)(?:\s*!\s*\(([^)]+)\))?', re.IGNORECASE)
    move_pattern = re.compile(r'([\w\s-]+) used ([\w\s-]+)!', re.IGNORECASE)
    opposing_move_pattern = re.compile(r'Opposing ([\w\s-]+) used ([\w\s-]+)!', re.IGNORECASE)

    def extract_valid_name(full_name, bracket_name):
        full_name = full_name.strip()
        bracket_name = bracket_name.strip() if bracket_name else None
        if full_name not in known_pokemon and bracket_name:
            return bracket_name
        return full_name

    # Process player's Pokémon
    for match in go_pattern.findall(battle_text):
        full_name, bracket_name = match
        chosen_name = extract_valid_name(full_name, bracket_name)

        # Look up the Pokémon in the DataFrame
        pokemon_row = pokemon_data[pokemon_data["Name"].str.strip() == chosen_name]
        if not pokemon_row.empty:
            row = pokemon_row.iloc[0]  # Get the first matching row
            
            # Check if the Pokémon is already in the player's list
            if not any(mon.name == row["Name"] for mon in field.playerMons):
                field.playerMons.append(Mon(
                    name=row["Name"],
                    type1=row["Type1"],
                    type2=row["Type2"],
                    HP=row["HP"],
                    Patk=row["Attack"],
                    Pdef=row["Defense"],
                    SpA=row["Special Attack"],
                    SpD=row["Special Defense"],
                    Speed=row["Speed"],
                    moves=[]
                ))
                print(f"Added player Pokémon: {chosen_name}")  # Debug output
                print("Current Player Pokémon List:", [mon.name for mon in field.playerMons])  # Debug output
            else:
                print(f"Player Pokémon already in list: {chosen_name}")  # Debug output
        else:
            print(f"Player Pokémon not found in DataFrame: {chosen_name}")  # Debug output

    # Process opponent's Pokémon
    for match in sent_out_pattern.findall(battle_text):
        full_name, bracket_name = match
        chosen_name = extract_valid_name(full_name, bracket_name)

        # Look up the Pokémon in the DataFrame
        pokemon_row = pokemon_data[pokemon_data["Name"].str.strip() == chosen_name]
        if not pokemon_row.empty:
            row = pokemon_row.iloc[0]  # Get the first matching row
            
            # Check if the Pokémon is already in the opponent's list
            if not any(mon.name == row["Name"] for mon in field.oppMons):
                field.oppMons.append(Mon(
                    name=row["Name"],
                    type1=row["Type1"],
                    type2=row["Type2"],
                    HP=row["HP"],
                    Patk=row["Attack"],
                    Pdef=row["Defense"],
                    SpA=row["Special Attack"],
                    SpD=row["Special Defense"],
                    Speed=row["Speed"],
                    moves=[]
                ))
                print(f"Added opponent Pokémon: {chosen_name}")  # Debug output
                print("Current Opponent Pokémon List:", [mon.name for mon in field.oppMons])  # Debug output
            else:
                print(f"Opponent Pokémon already in list: {chosen_name}")  # Debug output
        else:
            print(f"Opponent Pokémon not found in DataFrame: {chosen_name}")  # Debug output

    for match in move_pattern.findall(battle_text):
        pokemon_name, move = match
        for mon in field.playerMons:
            if mon.name == pokemon_name and move not in mon.Moves:
                mon.Moves.append(move)

    for match in opposing_move_pattern.findall(battle_text):
        pokemon_name, move = match
        for mon in field.oppMons:
            if mon.name == pokemon_name and move not in mon.moves:
                mon.moves.append(move)

def monitor_battle(field, known_pokemon):
    while any("Showdown!" in w.title for w in gw.getWindowsWithTitle("Showdown!")):
        battle_text = capture_chat()
        if battle_text:
            parse_battle_text(battle_text, field, known_pokemon)
        time.sleep(2)

try:
    field = Field()
    monitor_battle(field, known_pokemon)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Print the Pokémon lists after monitoring
    print("Final Player's Pokémon:", [mon.name for mon in field.playerMons])
    print("Final Opponent's Pokémon:", [mon.name for mon in field.oppMons])

