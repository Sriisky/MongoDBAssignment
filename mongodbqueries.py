import pymongo

from pymongo import ReturnDocument


client = pymongo.MongoClient('mongodb://admin:Sp00ky!@localhost:27017/?AuthSource=admin')
db = client.PokemonAssignment
collection = db.Pokemon
requesting = []

#Show all documents in JSON form
def all_docs():
    try:
            query = collection.find({})
            for document in query:
                print(document)
    except Exception as e:
            print("Error:", type(e), e)
        
#Show embedded data, select all pokemon of type fairy
def embedded_data():
    try:
        query = collection.find({"Typing.type_1" : "Fairy"})
        for document in query:
            print(document)
    except Exception as e:
                print("Error:", type(e), e)

#Select only the neccesary data instead of whole data set. return pokemon with egg type flying
def projection():
    try:
        query = collection.find({"Egg.egg_type_1" : "Flying"}, {"_id":0, "pokedex_number":1, "name":1})
        for document in query:
            print(document)
    except Exception as e:
                print("Error:", type(e), e)
                

#Sort all ghost pokemon in alphabetical order
def sort():
    try:
        query = collection.find({"Typing.type_1" : "Ghost"}, {"_id":0,"pokedex_number":1, "name":1}).sort([("name", 1)])
        for document in query:
            print(document)
    except Exception as e:
                print("Error:", type(e), e)
                
#Aggregation is a way of processing a large number of documents in a collection by means of passing them through different stages 
#return the number of psychic pokemon 
def pipeline():
    try:
        pipeline = [{
            "$unwind": "$Typing"},
            {"$match":{
                "Typing.type_1": "Psychic"
            }
        },
            {
                    "$count": "Psychic: "
                    },
            ]
        query = collection.aggregate(pipeline)
        for document in query:
                print(document)
    except Exception as e:
                print("Error:", type(e), e)

def insert():
    record_count = 0
    try:
        new_data = {
        "pokedex_number":1028,
        "name":"Pawmi",
        "german_name":"Pamo",
        "generation":9,
        "status":"Normal",
        "species":"Mouse Pokemon",
        "Typing":{
            "type_number":1,
            "type_1":"Electric",
            "type_2":""
        },
        "Abilities":{
            "abilities_number":2,
            "ability_1":"Scratch",
            "ability_2":'',
            "ability_hidden":"Iron fist"
        },
        "Stats":{
            "total_points":240,
            "hp":45,
            "attack":50,
            "sp_attack":40,
            "sp_defense":25,
            "speed":60,
            "catch_rate":35,
            "base_friendship":50.0,
            "base_experience":200.0,
            "growth_rate":"Slow"
        },
        "Egg":{
            "egg_type_number":2,
            "egg_type_1":"Grass",
            "egg_type_2":"Electric",
            "percentage_male":50.5,
            "egg_cycles":30.0
        },
        "Effectiveness":{
            "against_normal":1.0,
            "against_fire":1.0,
            "against_water":1.0,
            "against_electric":0.5,
            "against_grass":1.00,
            "against_ice":1.0,
            "against_fight":1.0,
            "against_poison":1.0,
            "against_ground":2.0,
            "against_flying":0.5,
            "against_psychic":1.0,
            "against_bug":1.0,
            "against_rock":1.0,
            "against_ghost":1.0,
            "against_dragon":1.0,
            "against_dark":1.0,
            "against_steel":0.5,
            "against_fairy":0.5
        }
    }
        
        
        query = collection.find({"name" : "Pawmi"})
        for document in query:
            record_count += 1
        if record_count == 0:
            insert_result = collection.insert_one(new_data)
            print("Entry has been inserted")
            query = collection.find({"name" : "Pawmi"}, {"_id":0,"pokedex_number":1, "name":1, "status":1})
            for document in query:
                print(document)
        else:
            print("Result is already in database")
            menu()
        
    except Exception as e:
     print("Error:", type(e), e)

def delete():
    try:
        record_count = 0
        query = collection.find({"name" : "Pawmi"})
        for document in query:
            record_count += 1
        if record_count >= 1:
            delete_result = collection.delete_one({"name" : "Pawmi" })
            print("Entry has been deleted")
        else:
            print("Result is not found in Database")
            menu()
    except Exception as e:
        print("Error:", type(e), e)
        
def update():
    try:
        record_count = 0
        query = collection.find({"name" : "Pawmi"})
        for document in query:
            record_count += 1
        if record_count >= 1:
            update_result = collection.find_one_and_update({"name": "Pawmi"}, {"$set": {"status": "Unreleased"}}, return_document=ReturnDocument.AFTER)
            print("Entry has been updated")
            query = collection.find({"name" : "Pawmi"}, {"_id":0,"pokedex_number":1, "name":1, "status":1})
            for document in query:
                print(document)
            
        else:
            print("Result is not found in Database")
            menu()
    except Exception as e:
        print("Error:", type(e), e)


#menu format to select options
def menu():
    print(" Pokemon Database Collection ")
    print(" ----------------------------------- ")

    choice = input("""
                      1: Display all documents
                      2: Display all fairy type Pokemon
                      3: Display Pokemon with flying egg type
                      4: Sort all ghost Pokemon in alphabetical order
                      5: Display the number of psychic Pokemon
                      6: Insert Pawmi
                      7: Delete Pawmi
                      8: Update Pawmi status
                      Q: Exit

                      Please enter your option: """)

    if choice == "1":
        all_docs()
        menu()
    elif choice == "2":
        embedded_data()
        menu()
    elif choice == "3":
        projection()
        menu()
    elif choice == "4":
        sort()
        menu()
    elif choice == "5":
        pipeline()
        menu()
    elif choice == "6":
        insert()
        menu()
    elif choice == "7":
        delete()
        menu()
    elif choice == "8":
        update()
        menu()
    elif choice=="Q" or choice=="q":
        exit()
    else:
        print("Invalid option")
        print("Please enter a value between 1-8 or Q to quit")
        menu()
menu()