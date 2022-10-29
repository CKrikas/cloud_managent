# importing the required libraries  
from sys import api_version
from time import sleep  
from json import dumps  
from kafka import KafkaProducer  
import requests

keywords = ["boxing", "gaming", "stocks", "nascar", "esports", "technology", "television", "greece"]
url = 'https://newsapi.org/v2/everything?q='

# initializing the Kafka producer 
my_producer = KafkaProducer(  
    api_version = (2, 0, 2),
    bootstrap_servers = ['localhost:9092'], 
    value_serializer = lambda x:dumps(x).encode('utf-8')  
    ) 

while(True):
    for i in keywords:
        currenturl = url+i
        articles = requests.get(currenturl, headers={"Authorization":"7ebcf37a46614529887f01dbb281e66c"})
        data = articles.json()
        my_producer.send(i, value = data)
        print("kafka producer did it's job, nice! Repeating in two hours\n")
    sleep(7200)