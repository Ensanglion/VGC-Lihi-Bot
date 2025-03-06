class Move:
    def __init__(self, name, BP, PP, type, category, contact, spread):
        self.name = name
        self.BP = BP
        self.PP = PP
        self.currentPP = PP
        self.type = type
        self.category = category
        self.contact = contact
        self.spread = spread

    def use_move(self):
        if self.currentPP > 0:
            self.currentPP -= 1
