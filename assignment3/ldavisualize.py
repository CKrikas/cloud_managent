import gensim
import pickle
import pyLDAvis.gensim

dictionary = gensim.corpora.Dictionary.load('model/dictionary.gensim')
corpus = pickle.load(open('model/corpus.pkl', 'rb'))
lda = gensim.models.ldamodel.LdaModel.load('model/model.gensim')
lda_display = pyLDAvis.gensim.prepare(lda, corpus, dictionary, sort_topics=False)

pyLDAvis.save_html(lda_display, 'lda_visualization.html')