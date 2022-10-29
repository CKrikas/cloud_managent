# importing the required libraries  
import os
from sys import api_version
from time import sleep  
from json import dumps, load  
from kafka import KafkaProducer
from dotenv import load_dotenv  
import requests

load_dotenv()

keywords = ["boxing", "gaming", "stocks", "nascar", "esports", "technology", "television", "greece"]
url = 'https://newsapi.org/v2/everything?q='

# initializing the Kafka producer 
my_producer = KafkaProducer(  
    bootstrap_servers = ['localhost:9092'], 
    value_serializer = lambda x:dumps(x).encode('utf-8')  
    ) 

while(True):
    for i in keywords:
        currenturl = url+i
        articles = requests.get(currenturl, headers={"Authorization":os.getenv('NEWSAPIKEY')})
        data = articles.json()
        my_producer.send(i, value = data)
    print("kafka producer did it's job, nice! Repeating in two hours\n")
    sleep(7200)