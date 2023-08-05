import numpy
from nltk.corpus import brown
import nltk

genres = ['news', 'religion', 'hobbies', 'science_fiction', 'romance', 'humor']


#brown_sents_label_pre=[[ [sent,g] for sent in nltk.corpus.brown.sents(categories=[g]) ] for g in genres]
cfd = nltk.ConditionalFreqDist( (genre, word) for genre in brown.categories()  for word in brown.words(categories=genre))
genres = ['news', 'religion', 'hobbies', 'science_fiction', 'romance', 'humor']
modals = ['can', 'could', 'may', 'might', 'must', 'will']
cfd.tabulate(conditions=genres, samples=modals)
