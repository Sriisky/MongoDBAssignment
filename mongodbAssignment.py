import pandas as pd # pandas handles panel data
import pymongo
import json
from pymongo import MongoClient, InsertOne

client = pymongo.MongoClient('mongodb://admin:Sp00ky!@localhost:27017/?AuthSource=admin')
#read in the csv file
df = pd.read_csv('pokedex.csv', encoding='utf-8-sig')
#Embedded arrays. Pick something that will be the main type and contain a list of items that may not be unique to go inside.
#create dataframes to organise data into rows and columns. embedded arrays
df['Typing'] = df[['type_number', 'type_1', 'type_2']].to_dict('records')
df['Abilities'] = df[['abilities_number', 'ability_1', 'ability_2', 'ability_hidden']].to_dict('records')
df['Stats'] = df[['total_points', 'hp', 'attack', 'sp_attack', 'sp_defense', 'speed', 'catch_rate', 'base_friendship', 'base_experience','growth_rate']].to_dict('records')
df['Egg'] = df[['egg_type_number', 'egg_type_1', 'egg_type_2', 'percentage_male', 'egg_cycles']].to_dict('records')
df['Effectiveness'] = df[['against_normal','against_fire','against_water','against_electric','against_grass','against_ice','against_fight','against_poison','against_ground','against_flying','against_psychic','against_bug','against_rock','against_ghost','against_dragon','against_dark','against_steel','against_fairy']].to_dict('records')
df[['pokedex_number','name','german_name','generation', 'status', 'species', 'Typing', 'Abilities', 'Stats', 'Egg', 'Effectiveness']].to_json (r'C:\Users\srisk\OneDrive - Technological University Dublin\Documents\YEAR 3 SEM 1\Databases2\Assignment2\pokedex.json', orient='records', indent=4)
db = client.PokemonAssignment
collection = db.Pokemon

#validation
if "Pokemon" in db.list_collection_names():
    collection.drop();
collection = db.create_collection(
    name = "Pokemon",
    validator = {"$jsonSchema": {
        "required": ["pokedex_number", "name", "generation"],
        "properties": {
            "pokedex_number": {
                "bsonType": "number",
                "description": "Unique identifier of every pokemon"
            },
            "name": {
                "bsonType": "string",
                "description": "Name of pokemon"
            },
            "generation": {
                "bsonType": "number",
                "description": "The era from which a pokemon is from"
            },
        }
        
    }},
    validationAction="error",)

#Ensure validation works correctly
#collection.insert_one(
#   {"pokedex_number":1029,
#   "name": "meowmeow"    
#});

#check and see if we can see any repeating values
poke= df[['pokedex_number','name', 'german_name']]
#print(poke.head(20)) #can see repeating pokemon in the german names

#print(df.dtypes) # column types

pokeName = df[['pokedex_number', 'german_name']].drop_duplicates().sort_values(['pokedex_number','german_name'], 
ascending = [True,True])
# Print the shape
#print(pokeName.shape) # 890, 2 this means there are a number of pokemon in the data set that have the same name in german
#print(pokeName.head(20)) #print first 20 non repeating pokemon 

#print(df.columns) #column names
#print(df.shape) #num of rows and columns, 1028 rows, 55 columns