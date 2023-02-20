
import nltk
import pandas as pd
import gensim
from gensim import corpora
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.tokenize import WordPunctTokenizer
from nltk.corpus import wordnet as wn
import time
import os
import pickle


en_stop = set(nltk.corpus.stopwords.words('english'))
tokenizer = WordPunctTokenizer()
dfsources = pd.read_csv('csv_files/domainNames.csv')
domain_names = dfsources['Domain Name'].values

def prepare_text_for_lda(text): # pre process the text for lda
    tokens = tokenizer.tokenize(text)
    tokens = [token for token in tokens if len(token) > 4] # shorter words are often function words or "noise", which are less informative for topic modeling
    tokens = [token for token in tokens if token not in en_stop] # remove common words that are usually not useful for analysis, such as "the", "a", "an"
    tokens = [token for token in tokens if token not in domain_names] # also remove source domain names from the articles titles cause some titles are in the form of "Title - by Source Domain"
    tokens = [token.lower() for token in tokens]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

def get_lemma(word): # function to get the "base form" of each word
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

def lda(path):
    st = time.time()
    text_data = []
    df = pd.read_csv(path)
    for title in df['Title']:
        tokens = prepare_text_for_lda(title)
        text_data.append(tokens)

    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    pickle.dump(corpus, open('model/corpus.pkl', 'wb'))
    dictionary.save('model/dictionary.gensim')

    NUM_TOPICS = 20 #number of topics to be generated
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=30)
    ldamodel.save('model/model.gensim')


    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')


if not os.path.exists('model'):
    os.makedirs('model')
lda('csv_files/allArticles.csv')