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
    bootstrap_servers="localhost:9092", 
    client_id='kafkaclient'
)

topic_list = [NewTopic(name=topic, num_partitions=1, replication_factor=1) for topic in ["boxing", "gaming", "stocks", "nascar", "esports", "technology", "television", "greece"] if topic not in admin_client.list_topics()]


admin_client.create_topics(new_topics=topic_list)

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