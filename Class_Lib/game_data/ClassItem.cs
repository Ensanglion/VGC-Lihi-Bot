using System;

namespace game_data
{
    public class Item
    {
        public string name;
        public bool consumable;

        public Item(string name, bool consumable)
        {
            this.name = name;
            this.consumable = consumable;
        }
    }
};

