import requests

#wikiextract = requests.get('https://en.wikipedia.org/w/api.php?action=query&prop=extracts&titles=BBC&exintro=True&explaintext=True&exsectionformat=plain&format=json').json()
newsresponse = requests.get('https://newsapi.org/v2/everything?q=boxing', headers={"Authorization":'7ebcf37a46614529887f01dbb281e66c'}).json()

def finditem(obj, key):
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = finditem(v, key)
            if item is not None:
                return item

#print(finditem(y, 'extract'))

names = []
articles = newsresponse['articles']
for article in articles:
    name = article['source']['name']
    names.append(name)

names = list(dict.fromkeys(names))
print(names)

url2 = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=True&explaintext=True&exsectionformat=plain&format=json&titles='
sourcedomains = {}
for sourcedomainname in names:
    wikiextract = requests.get(url2+sourcedomainname).json()
    description = finditem(wikiextract, 'extract')
    sourcedomains[sourcedomainname] = description

print(sourcedomains)