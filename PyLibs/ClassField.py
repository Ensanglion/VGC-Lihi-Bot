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
