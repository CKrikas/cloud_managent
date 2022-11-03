from flask import Flask, jsonify, request
import json
from pymongo import MongoClient 
import time

app = Flask(__name__)
my_client = MongoClient( 'localhost', 27017) 

@app.route('/create_user', methods = ['POST']) #link example http://localhost:7000/create_user
def process_json():
    data = json.loads(request.data) #data needs to come in the form of {"_id":"unique id", "keywords":"listofkeywords", "city":"cityname"} in json
    ts = time.time()
    data['timestamp'] = ts
    try: #user will only get added if he has unique id otherwise duplicate key error gets returned from mongodb
        my_client.kafkadb.users.insert_one(data)
        return 'User created successfully'
    except:
        return 'Username already taken'

@app.route('/user', methods = ['GET'])
def parse_request():
    uniqueID = request.args.get("id", default="") #link example http://localhost:7000/user?id=testuser123
    query = {"_id": uniqueID}
    cursor = my_client.kafkadb.users.find_one(query)
    try:
        articles = {}
        for keyword in cursor['keywords']:
            topicCollection = my_client['kafkadb'][keyword]
            cursor = topicCollection.find({})
            for article in cursor:
                del article['_id']
                tempDict = {}
                if article['source'] in articles: # articles = {"source name": {"description":"the description", "articles": [articles]}}
                    articles[article['source']]['articles'].append(article)
                else:
                    descriptioncursor = my_client.kafkadb.sourcesdomainname.find_one({"_id":article['source']})
                    description = descriptioncursor['description']
                    if description is None or 'refer to:' in description:
                        description = 'No description available for this source domain name'
                    tempDict['description'] = description
                    tempDict['articles'] = [article]
                    articles[article['source']] = tempDict
        return json.dumps(articles)
    except:
        return 'User not found'

@app.route('/update_user', methods = ['PUT']) #link example http://localhost:7000/update_user?id=testuser123
def update_keywords():
    uniqueID = request.args.get("id", default="")
    data = json.loads(request.data) #data needs to come in form of {"keywords":"listofkeywords"} in json
    query = {"_id": uniqueID}
    my_client.kafkadb.users.update_one(query, { "$set": data})
    return 'Successfully updated keywords'

@app.route('/delete_user', methods = ['DELETE']) #link example http://localhost:7000/delete_user?id=testuser123
def completely_obliterate_user():
    uniqueID = request.args.get("id", default="")
    query = {"_id": uniqueID}
    my_client.kafkadb.users.delete_one(query)
    return 'Successfully delete user'

if __name__ == "__main__":
    app.run(host="localhost", port=7000, debug=True)