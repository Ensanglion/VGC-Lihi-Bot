using System;

namespace game_data
{
    public class Move
    {
        public string name;
        public int BP;
        public int PP;
        public int currentPP; 
        public string type;
        public string category;
        public bool contact;
        public bool spread;

        public Move(string name, int BP, int PP, string type, string category, bool contact, bool spread)
        {
            this.name = name;
            this.BP = BP;
            this.PP = PP;
            this.currentPP = PP; 
            this.type = type;
            this.category = category;
            this.contact = contact;
            this.spread = spread;
        }

        public void UseMove()
        {
            if (currentPP > 0)
                currentPP--;
        }
    }
}
