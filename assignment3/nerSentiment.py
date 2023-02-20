import pandas as pd
import nltk
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')


df = pd.read_csv('csv_files/allArticles.csv')
dfsources = pd.read_csv('csv_files/domainNames.csv')
domain_names = dfsources['Domain Name'].str.lower().values

vader = SentimentIntensityAnalyzer()


def extract_entities(title): # Named entity recognition!
    entities = []
    tokens = nltk.word_tokenize(title)
    tokens = [token for token in tokens if token.lower() not in domain_names]
    #tokens = [token for token in tokens if len(token) > 4]
    tagged = nltk.pos_tag(tokens)
    named_entities = nltk.ne_chunk(tagged, binary=False)
    for ne in named_entities:
        if isinstance(ne, nltk.tree.Tree) and ne.label() in ['ORGANIZATION', 'PERSON', 'GPE']:
            entity = ' '.join([word for word, tag in ne.leaves()])
            entities.append(entity)
    return entities


all_entities = []
for title in df['Title']:
    entities = extract_entities(title)
    all_entities += entities


freq_entities = nltk.FreqDist(all_entities)
top_entities = freq_entities.most_common(15)


entity_scores = []
for entity, freq in top_entities: # Sentiment analysis on each of the most frequent entities
    scores = []
    for title in df['Title']:
        if entity in title:
            score = vader.polarity_scores(title)
            scores.append(score['compound'])
    if scores: # Add a check to ensure that the scores list is not empty
        avg_score = sum(scores) / len(scores)
        entity_scores.append((entity, avg_score))


entity_scores.sort(key=lambda x: x[1])

fig, ax = plt.subplots()
y_pos = range(len(entity_scores))
bars = ax.barh(y_pos, [score for entity, score in entity_scores], align='center', alpha=0.5)
ax.set_yticks(y_pos)
ax.set_yticklabels([entity for entity, score in entity_scores])
#ax.invert_yaxis() 
ax.set_xlabel('Sentiment Score')
ax.set_title('Sentiment Scores for Top Entities')


for i, bar in enumerate(bars):
    score = entity_scores[i][1]
    ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{score:.2f}', ha='left', va='center')

plt.show()
