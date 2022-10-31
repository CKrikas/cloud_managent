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
my_collection = my_client.kafkadb.test


while(True):
    for message in my_consumer:  
        message = message.value
        bigstatement = 'my_client.kafkadb.'+list((json.loads(message)).keys())[0]+'.insert_one(json.loads(message)[list(json.loads(message).keys())[0]])'
        eval(bigstatement)
        print("succesfully added to collection")

