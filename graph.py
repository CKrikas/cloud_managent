from pymongo import MongoClient 
import networkx as nx
import json
from bson import json_util
from datetime import datetime
from time import sleep
import time

my_client = MongoClient( 'localhost', 27017)  

while(True):
    st = time.time()
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
                if w8 > 0:
                    G.add_edge(nodeOut, nodeIn, weight = w8, timestampdif = abs(difference.total_seconds()))


    #print(G.number_of_nodes())
    #print(G.number_of_edges()) #nodes(nodes - 1) / 2 = number of edges


  
    noEdgeNodes = list(G.nodes)
    bestChoice = {} #Dictionary for every node and its best recommended article choice in the form of {"node": "best article choice"}
    for nodeOut in G.nodes:
        max = 0
        min = float('inf')
        bestsEdgeWeight = 0
        hasEdges = False
        for nodeIn in G.nodes:
            if nodeIn != nodeOut and G.has_edge(nodeOut, nodeIn):
                edge = G[nodeIn][nodeOut]
                WeightedNodeDegree = G.degree([nodeIn], weight='weight')[nodeIn]
                hasEdges = True
                if nodeOut in noEdgeNodes:
                    noEdgeNodes.remove(nodeOut)
                if WeightedNodeDegree > max:
                    max = WeightedNodeDegree
                    bestChoice[nodeOut] = nodeIn
                    bestsEdgeWeight = edge['weight']
                    min = edge['timestampdif']
                elif WeightedNodeDegree == max and edge['weight'] > bestsEdgeWeight:
                    max = WeightedNodeDegree
                    bestChoice[nodeOut] = nodeIn
                    bestsEdgeWeight = edge['weight']
                    min = edge['timestampdif']
                elif WeightedNodeDegree == max and edge['weight'] == bestsEdgeWeight and edge['timestampdif'] < min:
                    max = WeightedNodeDegree
                    bestChoice[nodeOut] = nodeIn
                    bestsEdgeWeight = edge['weight']
                    min = edge['timestampdif']

    timestamps = nx.get_node_attributes(G, "timestamp")
    for nodeOut in noEdgeNodes: #find the closest-to-the-original-node timestamp of the nodes with the highest WeightedNodeDegree
        min = float('inf')
        d1 = datetime.strptime(timestamps[nodeOut], '%Y-%m-%dT%H:%M:%SZ')
        for nodeIn,dataIn in G.nodes(data=True):
            d2 = datetime.strptime(dataIn['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
            difference = d2 - d1
            timestampdif = abs(difference.total_seconds())
            if timestampdif < min:
                min = timestampdif
                bestChoice[nodeOut] = nodeIn


    for article in bestChoice:
        query = {"_id": article}
        cursor = my_client.kafkadb.recommendations.find(query)
        try:
            cursor.next()
        except:
            my_client.kafkadb.recommendations.insert_one({"_id": article, "recommendation": bestChoice[article]})
    print("Successfully found every article's next best recommended article, repeating in 5 hours")
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
    sleep(18000) #repeat this process every 5 hours