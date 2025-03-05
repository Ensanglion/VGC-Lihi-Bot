using System;

namespace game_data
{
    public class Mon
    {
        public string name;
        public string type1;
        public string type2;
        public int HP;
        public double currentHP;
        public int Patk;
        public int Pdef;
        public int SpA;
        public int SpD;
        public int Speed;
        public Move move1;
        public Move move2;
        public Move move3;
        public Move move4;
        public Item heldItem;
        public string status;
        public string ability;
        public string teraType; 
        public bool IsTera;

        // Full constructor (for our Pokémon)
        public Mon(string name, string type1, string type2, int HP, int Patk, int Pdef, int SpA, int SpD, int Speed, Move move1, Move move2, Move move3, Move move4, Item heldItem, string status, string ability, string teraType)
        {
            this.name = name;
            this.type1 = type1;
            this.type2 = type2;
            this.HP = HP;
            this.currentHP = HP;
            this.Patk = Patk;
            this.Pdef = Pdef;
            this.SpA = SpA;
            this.SpD = SpD;
            this.Speed = Speed;
            this.move1 = move1;
            this.move2 = move2;
            this.move3 = move3;
            this.move4 = move4;
            this.heldItem = heldItem;
            this.status = status;
            this.ability = ability;
            this.teraType = teraType;
            this.IsTera = false;
        }

        // Opponent's constructor (without moves, item, or teraType)
        public Mon(string name, string type1, string type2, int HP, int Patk, int Pdef, int SpA, int SpD, int Speed, string status, string ability)
        {
            this.name = name;
            this.type1 = type1;
            this.type2 = type2;
            this.HP = HP;
            this.currentHP = HP;
            this.Patk = Patk;
            this.Pdef = Pdef;
            this.SpA = SpA;
            this.SpD = SpD;
            this.Speed = Speed;
            this.status = status;
            this.ability = ability;
            

            this.move1 = null;
            this.move2 = null;
            this.move3 = null;
            this.move4 = null;
            this.heldItem = null;
            this.teraType = null;
            this.IsTera = false;
        }
    }
}
