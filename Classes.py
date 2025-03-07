class Mon:
    def __init__(self, name, type1, type2, HP, Patk, Pdef, SpA, SpD, Speed, 
                 move1=None, move2=None, move3=None, move4=None, 
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
        self.move1 = move1
        self.move2 = move2
        self.move3 = move3
        self.move4 = move4
        self.heldItem = heldItem
        self.status = status
        self.ability = ability
        self.teraType = teraType
        self.IsTera = False

    def take_damage(self, damage):
        damage = damage/100
        self.currentHP -= damage


class Field:
    def __init__(self, playerLeft=None, playerRight=None, oppLeft=None, oppRight=None):
        self.playerLeft = playerLeft
        self.playerRight = playerRight
        self.oppLeft = oppLeft
        self.oppRight = oppRight
        
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
