# importing the required libraries  
import os
from sys import api_version
from time import sleep  
from json import dumps, load  
from kafka import KafkaProducer
from dotenv import load_dotenv  
import requests
import json

load_dotenv()

keywords = ["boxing", "gaming", "stocks", "nascar", "esports", "technology", "television", "greece"]
url = 'https://newsapi.org/v2/everything?q='
url2 = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=True&explaintext=True&exsectionformat=plain&format=json&titles='

# initializing the Kafka producer 
my_producer = KafkaProducer(  
    bootstrap_servers = ['localhost:9092'], 
    value_serializer = lambda x:dumps(x).encode('utf-8')
    ) 

def findextract(obj, key):  #recursive function that finds a key and returns the value in a dictionary
    if key in obj: return obj[key]  #needed because the wiki extract is at the bottom of some nested dictionaries
    for k, v in obj.items():
        if isinstance(v,dict):
            item = findextract(v, key)
            if item is not None:
                return item

while(True):
    for i in keywords:
        currenturl = url+i
        articles = requests.get(currenturl, headers={"Authorization":os.getenv('NEWSAPIKEY')})
        data = {}
        data[i] = articles.json() #now each message will have the topic it belongs to in it
        my_producer.send(i, value = json.dumps(data)) #send articles to their corresponding topic

        names = [] #making a list with the source domain names from each article
        articles = data[i]['articles']
        for article in articles:
            name = article['source']['name']
            names.append(name)
        names = list(dict.fromkeys(names)) #remove duplicates names

        sourcedomains = {}  #get the description of each source domain from wikipedia and make a dictionary {source domain name: description}
        sourcesdomainnameTopic = {}
        for name in names:
            wikiextract = requests.get(url2+name).json()
            description = findextract(wikiextract, 'extract')
            sourcedomains[name] = description
        sourcesdomainnameTopic['sourcesdomainname'] = json.dumps(sourcedomains) #same as before, send source domain dictionary with descriptions, in a dictionary where the key is the topic it belongs to and the value is the dictionary with the sources and the descriptions
        my_producer.send("sourcesdomainname", value = json.dumps(sourcesdomainnameTopic)) #sending source domain dictionary to the sourcedomains topic
    print("kafka producer did it's job, nice! Repeating in two hours\n")
    sleep(7203)