class Mon:
    def __init__(self, name, type1, type2, HP, Patk, Pdef, SpA, SpD, Speed, 
                 moves=None, 
                 heldItem=None, status="", ability="", teraType=None):
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

    def take_damage(self, damage):
        damage = damage/100
        self.currentHP -= damage

    def modify_stats(self, stat_changes):
        """Modify the stats of the Mon based on the provided changes."""
        for stat, change in stat_changes.items():
            if stat == "Patk":
                self.Patk += change
            elif stat == "Pdef":
                self.Pdef += change
            elif stat == "SpA":
                self.SpA += change
            elif stat == "SpD":
                self.SpD += change
            elif stat == "Speed":
                self.Speed += change
    
    def add_move(self, move_name):
        """Adds a move to the Pokémon's move list if it has space."""
        if len(self.Moves) < 4 and move_name not in [m.name for m in self.Moves]:
            self.Moves.append(Move(name=move_name, BP=0, PP=0, type="Normal", category="Status", contact=False, spread=False, priority=0))


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
    def __init__(self, name, BP, PP, type, category, contact, spread, priority):
        self.name = name
        self.BP = BP
        self.PP = PP
        self.currentPP = PP
        self.type = type
        self.category = category
        self.contact = contact
        self.spread = spread
        self.priority = priority

    def use_move(self):
        if self.currentPP > 0:
            self.currentPP -= 1
