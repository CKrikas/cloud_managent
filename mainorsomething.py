# importing the required libraries  
from time import sleep  
from json import dumps  
from kafka import KafkaProducer 
from kafka.admin import KafkaAdminClient, NewTopic
from threading import *
from multiprocessing import Process
import os
import logging

logging.basicConfig(level=logging.DEBUG)
admin_client = KafkaAdminClient(
    api_version = (2, 0, 2),
    bootstrap_servers="localhost:9092", 
    client_id='kafkaclient'
)

topic_list = ["boxing", "gaming", "stocks", "nascar", "esports", "technology", "television", "greece"]
#topic_list.append(NewTopic(name="example_topic", num_partitions=1, replication_factor=1))
admin_client.create_topics(new_topics=topic_list, validate_only=False)

def producerprocess():
    os.system('python3 producer.py') 

def consumerprocess():
    os.system('python3 consumer.py')

print("Starting producer...")
p1 = Process(target = producerprocess, args=())
sleep(3)
print("Starting consumer...")
p2 = Process(target = consumerprocess, args=())

p1.start()
p2.start()
p1.join()
p2.join()