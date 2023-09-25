import pymongo
import json
from pymongo import MongoClient, InsertOne

client = pymongo.MongoClient('mongodb://admin:Sp00ky!@localhost:27017/?AuthSource=admin')
db = client.PokemonAssignment
collection = db.Pokemon
requesting = []

#inserting data 
with open(r"pokedex.json") as i:
        myData = json.loads(i.read())
        record_count = 0
        query = collection.find({"name" : "Sylveon"})
        for document in query:
            record_count += 1
        if record_count >= 1:
                print("Data has already been entered into database")
        else:
             collection.insert_many(myData)

client.close()