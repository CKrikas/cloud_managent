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
        try: #try block sorts articles into their respective collections whereas except block sorts source domain names and their descriptions into the sourcesdomainname collection
            topicname = list((json.loads(message)).keys())[0]
            articles = json.loads(message)[topicname]['articles']
            for article in articles:
                article['source'] = article['source']['name']
                query = {"title": article['title']}
                cursor = my_client.kafkadb.topicname.find(query)
                try: 
                    cursor.next() #This either fails if the article isn't in the database therefore going into the except statement and adding it in or it skips it
                except: #insert the article into its respective collection and also insert it into a collection that has ALL the artiles
                    bigstatement = 'my_client.kafkadb.'+topicname+'.insert_one(article)'
                    eval(bigstatement)
                    article['topic'] = topicname
                    insertintoAllArticlesCollection = my_client.kafkadb.allArticles.insert_one(article)
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

