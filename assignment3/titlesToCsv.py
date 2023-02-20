import csv
import os
from pymongo import MongoClient
import pandas as pd

client = MongoClient('localhost', 27017)
db = client['kafkadb']
collection = db['allArticles']
sources = db['sourcesdomainname']

csv_path = 'csv_files/allArticles.csv' #check if file exists, if not, create a new csv file with the first row being the column name
if not os.path.isfile(csv_path):
    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Title'])

data = []
for document in collection.find():
    row = [document['title']]
    data.append(row)

with open(csv_path, 'a', newline='') as file: #append data to already existing csv file
    writer = csv.writer(file)
    writer.writerows(data)


names = []
for document in sources.find():
    row = [document['_id']]
    names.append(row)
    
with open('csv_files/domainNames.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Domain Name'])
    writer.writerows(names)

data = pd.read_csv(csv_path)
duplicates = data.duplicated()
data = data.drop_duplicates()
data.to_csv(csv_path, index=False)