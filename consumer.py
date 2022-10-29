# importing the required modules  
from json import loads  
from kafka import KafkaConsumer  
from pymongo import MongoClient 

# generating the Kafka Consumer  
my_consumer = KafkaConsumer(
    *["boxing", "gaming", "stocks", "nascar", "esports", "technology", "television", "greece"],  
    bootstrap_servers = ['localhost : 9092'], 
    client_id = 'kafkaclient', 
    auto_offset_reset = 'earliest',
    group_id = 'consumers',
    enable_auto_commit = True,    
    value_deserializer = lambda x : loads(x.decode('utf-8'))  
    ) 

my_client = MongoClient( 'localhost', 27017, username='root', password='example')  
my_collection = my_client.db.test

while(True):
    for message in my_consumer:  
        message = message.value  
        my_collection.insert_one(message)  
        print("succesfully added to collection")  