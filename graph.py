from pymongo import MongoClient 
import networkx as nx
import json
from bson import json_util
from datetime import datetime
from time import sleep

my_client = MongoClient( 'localhost', 27017)  

while(True):
    G = nx.Graph()
    n = 0
    for article in my_client.kafkadb.allArticles.find():
        nodename = json.loads(json_util.dumps(article['_id']))['$oid']
        G.add_node(nodename, source = article['source'], author = article['author'], timestamp = article['publishedAt'])


    for nodeOut,dataOut in G.nodes(data=True):
        d1 = datetime.strptime(dataOut['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
        for nodeIn,dataIn in G.nodes(data=True):
            d2 = datetime.strptime(dataIn['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
            if nodeIn != nodeOut:
                w8 = 0
                if dataIn['source'] == dataOut['source']:
                    w8 = w8+1
                if dataIn['author'] == dataOut['author']:
                    w8 = w8+1
                difference = d2 - d1
                G.add_edge(nodeOut, nodeIn, weight = w8, timestampdif = abs(difference.total_seconds()))


    #print(G.number_of_nodes())
    #print(G.number_of_edges()) #nodes(nodes - 1) / 2 = number of edges


    ''' This works but... it's slow and probably not the most efficient method'''
    bestChoice = {} #Dictionary for every node and its best recommended article choice in the form of {"node": "best article choice"}
    for nodeOut in G.nodes:
        max = 0
        min = float('inf')
        bestsEdgeWeight = 0
        for nodeIn in G.nodes:
            if nodeIn != nodeOut:
                WeightedNodeDegree = G.degree([nodeIn], weight='weight')[nodeIn]
                edge = G[nodeIn][nodeOut]
                if WeightedNodeDegree > max and edge['weight'] > 0:
                    max = WeightedNodeDegree
                    bestChoice[nodeOut] = nodeIn
                    bestsEdgeWeight = edge['weight']
        for nodeIn in G.nodes: #find the closest-to-the-original-node timestamp of the nodes with the highest WeightedNodeDegree
            if nodeIn != nodeOut:
                WeightedNodeDegree = G.degree([nodeIn], weight='weight')[nodeIn]
                edge = G[nodeIn][nodeOut]
                if WeightedNodeDegree == max and edge['timestampdif'] <= min and edge['weight'] == bestsEdgeWeight:
                    min = edge['timestampdif']
                    bestChoice[nodeOut] = nodeIn

    for article in bestChoice:
        my_client.kafkadb.recommendations.insert_one({"_id": article, "recommendation": bestChoice[article]})
    print("Successfully found every article's next best recommended article, repeating in 5 hours")
    sleep(18000) #repeat this process every 5 hours