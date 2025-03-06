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
