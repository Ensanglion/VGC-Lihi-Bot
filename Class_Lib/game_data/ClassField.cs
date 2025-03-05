using System;

namespace game_data
{
    public class Field
    {
        public Mon playerLeft;
        public Mon playerRight;
        public Mon oppLeft;
        public Mon oppRight;
        public bool TrickRoom;
        public bool playerTailwind;
        public bool oppTailwind;
        public string terrain;  
        public bool playerReflect;
        public bool playerLightScreen;
        public bool playerSafeguard;
        public bool playerStealthRock;
        public bool playerSpikes;
        public bool playerToxicSpikes;
        public bool playerStickyWeb;
        public bool playerAuroraVeil;
        public bool oppReflect;
        public bool oppLightScreen;
        public bool oppSafeguard;
        public bool oppStealthRock;
        public bool oppSpikes;
        public bool oppToxicSpikes;
        public bool oppStickyWeb;
        public bool oppAuroraVeil;
        public string weather;  

        public Field(Mon playerLeft, Mon playerRight, Mon oppLeft, Mon oppRight)
        {
            this.playerLeft = null;
            this.playerRight = null;
            this.oppLeft = null;
            this.oppRight = null;
            
            this.TrickRoom = false;
            this.playerTailwind = false;
            this.oppTailwind = false;
            this.terrain = null;
            this.playerReflect = false;
            this.playerLightScreen = false;
            this.playerSafeguard = false;
            this.playerStealthRock = false;
            this.playerSpikes = false;
            this.playerToxicSpikes = false;
            this.playerStickyWeb = false;
            this.playerAuroraVeil = false;
            this.oppReflect = false;
            this.oppLightScreen = false;
            this.oppSafeguard = false;
            this.oppStealthRock = false;
            this.oppSpikes = false;
            this.oppToxicSpikes = false;
            this.oppStickyWeb = false;
            this.oppAuroraVeil = false;
            this.weather = null;
        }
    };
}