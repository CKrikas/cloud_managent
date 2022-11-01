# importing the required modules  
from json import loads
import json
from sys import api_version  
from kafka import KafkaConsumer  
from pymongo import MongoClient 
from time import sleep

# generating the Kafka Consumer  
my_consumer = KafkaConsumer(
    *["boxing", "gaming", "stocks", "nascar", "esports", "technology", "television", "greece", "sourcesdomainname"],  
    bootstrap_servers = ['localhost:9092'],
    client_id = 'kafkaclient', 
    auto_offset_reset = 'earliest',
    group_id = 'consumers',
    enable_auto_commit = True,    
    value_deserializer = lambda x : loads(x.decode('utf-8'))  
    ) 

my_client = MongoClient( 'localhost', 27017)  


while(True):
    for message in my_consumer:  
        message = message.value
        try:
            middle = list((json.loads(message)).keys())[0]
            bigstatement = 'my_client.kafkadb.'+middle+'.insert_one(json.loads(message)[list(json.loads(message).keys())[0]])'
            eval(bigstatement)
        except:
            newmessage = json.loads(message)
            domaindata = json.loads(newmessage['sourcesdomainname'])

            for name in domaindata:
                query = {name: {"$exists": True}}
                cursor = my_client.kafkadb.sourcesdomainname.find(query)
                try:
                    cursor.next()
                except:
                    myquery = {"foo":"bar"}
                    newvalues = { "$set": { name: domaindata[name]}}
                    my_client.kafkadb.sourcesdomainname.update_one(myquery, newvalues, upsert=True)
        print("succesfully added to collection")

