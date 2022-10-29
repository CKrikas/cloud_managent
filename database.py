import pymongo

client = pymongo.MongoClient()

db = client["db"]

mycol = db["test"]