import pandas as pd

def load_move_data(csv_path="Move_Data.csv"):
    """Load move data from a CSV file into a dictionary."""
    move_data = {}
    try:
        df = pd.read_csv(csv_path)
        for _, row in df.iterrows():
            move_data[row["Name"].strip()] = {
                "BP": row["BP"],
                "PP": row["PP"],
                "type": row["type"],
                "accuracy": row["accuracy"],
                "category": row["category"],
                "contact": row["contact"] == "TRUE",
                "spread": row["spread"] == "TRUE",
                "priority": row["priority"]
            }
    except Exception as e:
        print(f"Error loading move data: {e}")
    return move_data


class Mon:
    def __init__(self, name, type1, type2, HP, Patk, Pdef, SpA, SpD, Speed, 
                 moves=None, 
                 heldItem=None, status="", ability="", teraType=None, extra_effects=None):
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.HP = HP
        self.currentHP = HP
        self.Patk = Patk
        self.Pdef = Pdef
        self.SpA = SpA
        self.SpD = SpD
        self.Speed = Speed
        self.Moves = moves if moves else [] # Initialize with empty list if no moves are provided
        self.heldItem = heldItem
        self.status = status
        self.ability = ability
        self.teraType = teraType
        self.IsTera = False
        self.extra_effects = extra_effects if extra_effects else [] # Initialize with empty list if no effects are provided
        
        # Store original stats for comparison
        self.original_stats = {
            "Patk": Patk,
            "Pdef": Pdef,
            "SpA": SpA,
            "SpD": SpD,
            "Speed": Speed
        }

    def take_damage(self, damage):
        damage = damage/100
        self.currentHP -= damage

    def modify_stats(self, stat_changes):
        """Modify the stats of the Mon based on the provided changes."""
        for stat, change in stat_changes.items():
            if stat == "Patk":
                self.Patk *= change
            elif stat == "Pdef":
                self.Pdef *= change
            elif stat == "SpA":
                self.SpA *= change
            elif stat == "SpD":
                self.SpD *= change
            elif stat == "Speed":
                self.Speed *= change
    
    def add_move(self, move_name, move_data):
        """Adds a move to the Pokémon's move list if it has space."""
        if len(self.Moves) < 4 and move_name in move_data:
            move_info = move_data[move_name]
            self.Moves.append(Move(
                name=move_name,
                BP=move_info["BP"],
                PP=move_info["PP"],
                type=move_info["type"],
                accuracy=move_info["accuracy"],
                category=move_info["category"],
                contact=move_info["contact"],
                spread=move_info["spread"],
                priority=move_info["priority"]
            ))

    def stats_raised(self):
        """Check if any stats have been raised above their original values."""
        return (self.Patk > self.original_stats["Patk"] or
                self.Pdef > self.original_stats["Pdef"] or
                self.SpA > self.original_stats["SpA"] or
                self.SpD > self.original_stats["SpD"] or
                self.Speed > self.original_stats["Speed"])

class Field:
    def __init__(self, playerMons=None, oppMons=None):
        # Initialize with empty lists if no Mons are provided
        self.playerMons = playerMons if playerMons is not None else []
        self.oppMons = oppMons if oppMons is not None else []
        
        # Initialize other attributes as needed
        self.TrickRoom = False
        self.playerTailwind = False
        self.oppTailwind = False
        self.terrain = None
        self.playerReflect = False
        self.playerLightScreen = False
        self.playerSafeguard = False
        self.playerStealthRock = False
        self.playerSpikes = False
        self.playerToxicSpikes = False
        self.playerStickyWeb = False
        self.playerAuroraVeil = False
        self.oppReflect = False
        self.oppLightScreen = False
        self.oppSafeguard = False
        self.oppStealthRock = False
        self.oppSpikes = False
        self.oppToxicSpikes = False
        self.oppStickyWeb = False
        self.oppAuroraVeil = False
        self.weather = None

class Item:
    def __init__(self, name, consumable, removable):
        self.name = name
        self.consumable = consumable
        self.removable = removable


class Move:
    def __init__(self, name, BP, PP, type, accuracy, category, contact, spread, priority):
        self.name = name
        self.BP = BP
        self.PP = PP
        self.currentPP = PP
        self.type = type
        self.accuracy = accuracy
        self.category = category
        self.contact = contact
        self.spread = spread
        self.priority = priority

    def use_move(self):
        if self.currentPP > 0:
            self.currentPP -= 1
