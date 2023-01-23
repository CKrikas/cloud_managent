import matplotlib.pyplot as plt
from pymongo import MongoClient 
from datetime import timedelta
from datetime import datetime
import pandas as pd

my_client = MongoClient( 'localhost', 27017)


days4ago = (datetime.today() - timedelta(days=4)).day
days3ago = (datetime.today() - timedelta(days=3)).day
days2ago = (datetime.today() - timedelta(days=2)).day
days1ago = (datetime.today() - timedelta(days=1)).day
today = datetime.today().day
x = [days4ago, days3ago, days2ago, days1ago, today]

cursor = my_client.kafkadb.allArticles.find()
sums = {"boxing":0, "gaming":0, "stocks":0, "nascar":0, "esports":0, "technology":0, "television":0, "greece":0}
df = pd.DataFrame.from_dict(sums, orient='index')
for day in x:
    df[day] = 0
n = 0
for article in cursor:
    n = n+1
    timestamp = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
    diff = abs((timestamp - datetime.today()).total_seconds())
    topic = article['topic']
    if diff <= 86400:
        df[today][topic] = df[today][topic]+1
    elif diff > 86400 and diff <= 172800:
        df[days1ago][topic] = df[days1ago][topic] + 1
    elif diff > 172800 and diff <= 259200:
        df[days2ago][topic] = df[days2ago][topic] + 1
    elif diff > 259200 and diff <= 345600:
        df[days3ago][topic] = df[days3ago][topic] + 1
    elif diff > 345600 and diff <= 432000:
        df[days4ago][topic] = df[days4ago][topic] + 1


df = df.T
ax = df.plot(kind='bar', stacked=True, title='Stacked Bar Graph', xlabel='Day', ylabel='Count')
for c in ax.containers:
    labels = [v.get_height() if v.get_height() > 0 else '' for v in c]
    ax.bar_label(c, labels=labels, label_type='center')
plt.show()