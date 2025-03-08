import threading
import time
import pandas as pd
import re
from Classes import Mon, Field
from screenshot import capture_chat

# Load known Pokémon names from CSV
def load_pokemon_names(csv_path="Pokemon_Data.csv"):
    """Loads Pokémon names from the CSV file into a set."""
    try:
        df = pd.read_csv(csv_path)
        return set(df["Name"].str.strip())  # Ensure names are stripped of spaces
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return set()

known_pokemon = load_pokemon_names()

# Updated function to parse battle text
def parse_battle_text(battle_text, field, known_pokemon):
    """
    Parses battle text to extract Pokémon names correctly and add them to the list.
    Ensures names with spaces (like 'Iron Hands') are fully captured.
    If the Pokémon name isn't in the dataset and has brackets next to it, 
    it uses the name inside the brackets.
    """
    # Updated regex patterns to correctly capture full names before '!' or inside brackets
    go_pattern = re.compile(r'Go!\s*([\w\s-]+?)(?=\s*!|\s*\()', re.IGNORECASE)
    sent_out_pattern = re.compile(r'sent out\s*([\w\s-]+?)(?=\s*!|\s*\()', re.IGNORECASE)
    bracketed_name_pattern = re.compile(r'\(([^)]+)\)')  # Extracts anything inside parentheses

    def extract_valid_name(full_name, text_after):
        full_name = full_name.strip()
        
        # Check if there is a bracketed name
        bracketed_match = bracketed_name_pattern.search(text_after)
        bracketed_name = bracketed_match.group(1).strip() if bracketed_match else None

        # Use bracketed name if full_name isn't recognized and bracket_name exists in known Pokémon
        if full_name not in known_pokemon and bracketed_name and bracketed_name in known_pokemon:
            return bracketed_name
        return full_name

    # Process player Pokémon
    for match in go_pattern.finditer(battle_text):
        full_name = match.group(1)
        text_after = battle_text[match.end():]  # Get text after the Pokémon name

        if full_name:
            chosen_name = extract_valid_name(full_name, text_after)
            if not any(mon.name == chosen_name for mon in field.playerMons):
                field.playerMons.append(Mon(name=chosen_name, type1="Normal", type2="None", HP=100, Patk=50, Pdef=50, SpA=50, SpD=50, Speed=50))

    # Process opponent Pokémon
    for match in sent_out_pattern.finditer(battle_text):
        full_name = match.group(1)
        text_after = battle_text[match.end():]  # Get text after the Pokémon name

        if full_name:
            chosen_name = extract_valid_name(full_name, text_after)
            if not any(mon.name == chosen_name for mon in field.oppMons):
                field.oppMons.append(Mon(name=chosen_name, type1="Normal", type2="None", HP=100, Patk=50, Pdef=50, SpA=50, SpD=50, Speed=50))

# Background monitoring function
def monitor_battle(field, known_pokemon):
    while True:
        battle_text = capture_chat()
        if battle_text:
            parse_battle_text(battle_text, field, known_pokemon)
        time.sleep(2)

# Initialize
field = Field()

# Start background thread
monitor_thread = threading.Thread(target=monitor_battle, args=(field, known_pokemon))
monitor_thread.daemon = True
monitor_thread.start()

# Main loop for debugging
while True:
    print(f"Player's Pokémon: {[mon.name for mon in field.playerMons]}")
    print(f"Opponent's Pokémon: {[mon.name for mon in field.oppMons]}")
    time.sleep(10)
