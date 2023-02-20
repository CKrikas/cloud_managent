# importing the required modules  
from json import loads
import json
from sys import api_version  
from kafka import KafkaConsumer  
from pymongo import MongoClient 
from time import sleep

# generating the Kafka Consumer  
my_consumer = KafkaConsumer(
    *["artificial_intelligence", "ai", "microsoft", "google", "chatgpt", "technology", "data_science", "deep_learning",
            "robotics", "automation", "cybersecurity", "blockchain", "fintech", "virtual_reality", "augmented_reality", "self_driving_cars",
            "big_data", "cloud_computing", "quantum_computing", "apple", "computer_vision", "neural_networks", "amazon", "data_mining",
             "tesla", "meta", "FANG", "FAANG", "bing", "layoffs", "twitter", "nanotechnology", "sourcesdomainname"],  
    bootstrap_servers = ['localhost:9092'],
    client_id = 'kafkaclient', 
    auto_offset_reset = 'earliest',
    group_id = 'consumers',
    enable_auto_commit = True,    
    value_deserializer = lambda x : loads(x.decode('utf-8'))  
) 

my_client = MongoClient('localhost', 27017)

while True:
    for message in my_consumer:
        message = message.value
        try:
            topicname = list(json.loads(message).keys())[0]
            articles = json.loads(message)[topicname]['articles']
            for article in articles:
                article['source'] = article['source']['name']
                query = {'url': article['url']}
                if not my_client.kafkadb[topicname].count_documents(query):
                    my_client.kafkadb[topicname].insert_one(article)
                    article['topic'] = topicname
                    my_client.kafkadb.allArticles.insert_one(article)
        except:
            newmessage = json.loads(message)
            domaindata = json.loads(newmessage['sourcesdomainname'])
            for name in domaindata:
                try:
                    if domaindata[name] is None or 'refer to:' in domaindata[name] or domaindata[name]=='':
                        domaindata[name] = 'No description available for this source domain name'
                    my_client.kafkadb.sourcesdomainname.insert_one({"_id": name, "description": domaindata[name]})
                except:
                    continue
        print("Successfully added to collection")