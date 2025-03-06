from Classes import Mon 
import pandas as pd

# Example DataFrame
data = {
    "name": ["Miraidon"],
    "type1": ["Electric"],
    "type2": ["Dragon"],
    "HP": [100],
    "Patk": [85],
    "Pdef": [100],
    "SpA": [165],
    "SpD": [120],
    "Speed": [135],
    "ability": ["Hadron Engine"]
}

df = pd.DataFrame(data)

# Creating a Mon object using DataFrame values
miraidon = Mon(
    name=df.loc[0, "name"],
    type1=df.loc[0, "type1"],
    type2=df.loc[0, "type2"],
    HP=df.loc[0, "HP"],
    Patk=df.loc[0, "Patk"],
    Pdef=df.loc[0, "Pdef"],
    SpA=df.loc[0, "SpA"],
    SpD=df.loc[0, "SpD"],
    Speed=df.loc[0, "Speed"],
    status="Healthy",
    ability=df.loc[0, "ability"]
)

print(miraidon.name, miraidon.ability, miraidon.SpA)
