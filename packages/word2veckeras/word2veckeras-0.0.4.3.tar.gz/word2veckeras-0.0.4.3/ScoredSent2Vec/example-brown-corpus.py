#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html


import logging
import sys
import os
from word2vec import Word2Vec, Sent2Vec, LineSentence, LineScoredSentence, ScoredSent2Vec
import nltk
import numpy
from random import shuffle


def mysentscore1(sent,scale):
    mywords=['can', 'could', 'may', 'might', 'must', 'will']
    return  [sent.count(w)*scale for w in mywords]

genres = ['news', 'religion', 'hobbies', 'science_fiction', 'romance', 'humor']

#brown_sents_genres=[[nltk.corpus.brown.sents(categories=[g]),g]  for g in genres]
#brown_sents_genres=[[nltk.corpus.brown.sents(categories=[g]),g]  for g in genres]
brown_sents_label_pre=[[ [sent,g] for sent in nltk.corpus.brown.sents(categories=[g]) ] for g in genres]

#print brown_sents_label_pre[0][0]

brown_sents_labels=[]
for n in range(len(genres)):
    brown_sents_labels.extend(brown_sents_label_pre[n])

#print brown_sents_label[1]
#sents=[sent_label[0] for sent_label in brown_sents_labels]
#print sents



def test_sentvec(sg_v,scale):

#sents_scores=[[s,mysentscore1(s)] for s in sents]

    sents_scores_labels=[[sl[0],mysentscore1(sl[0],scale),sl[1]] for sl  in brown_sents_labels]
    print len(sents_scores_labels)

    #print sents_scores_labels[0]
    #print sents_scores_labels[1]

    #sents_scores_labels2 = numpy.random.shuffle(sents_scores_labels)
    shuffle(sents_scores_labels)

    sents_scores=[[scl[0],scl[1]] for scl in sents_scores_labels]
    sents=[scl[0] for scl in sents_scores_labels]

    # print sents_scores_labels[0]
    # print sents_scores_labels[1]

    # print sents_scores[0]
    # print sents_scores[1]


    # sys.exit(0)




    #sg_v=0
    #sg_v=1

    modelbrw = Word2Vec(sents , size=100, window=5, sg=sg_v, min_count=5, workers=8)
    modelbrw.save('braword.model')
    modelbrw.save_word2vec_format('braword.vec')

    modelbrsc = ScoredSent2Vec(sents_scores, model_file='braword.model',sg=sg_v)
    modelbrsc.save_sent2vec_format('brasentsc.vec')

    modelbrs = Sent2Vec(sents, model_file='braword.model',sg=sg_v)
    modelbrs.save_sent2vec_format('brasent.vec')



    N=len(brown_sents_labels)
    #X=numpy.array([modelbrs.sents[n] for n in range(N)])
    X1 =[modelbrs.sents[n] for n in range(N)]
    X2 =[modelbrsc.sents[n] for n in range(N)]
    X3 =[numpy.append(modelbrs.sents[n],sents_scores[n][1])  for n in range(N)]
    #Y=[brown_sents_labels[n][1] for n in range(N)]
    Y=[scl[2] for scl in sents_scores_labels]
    #print Y2

    #print X2[0]
    #print X3[0]
    #print X[0]
    #print Y[1]



    from sklearn.linear_model import LogisticRegression
    from sklearn.cross_validation import cross_val_score

    # logreg = LogisticRegression() #C=1e5)
    # logreg.fit(X, Y)
    # print logreg.predict(X[0])




    scores= cross_val_score(LogisticRegression(), X1, Y, scoring='accuracy', cv=5)
    ret1=scores.mean()
    #sg=0 [ 0.53975265  0.51620507  0.57984679  0.52477876  0.53628319]
    #sg=1 [ 0.54240283  0.51738362  0.58603418  0.52330383  0.55103245]


    scores = cross_val_score(LogisticRegression(), X2, Y, scoring='accuracy', cv=5)
    ret2=scores.mean()
    #sg=0 [ 0.63309776  0.68031821  0.71243371  0.69852507  0.67758112]
    #sg=1 [ 0.64163722  0.69799646  0.72156747  0.70707965  0.69085546]

    scores = cross_val_score(LogisticRegression(), X3, Y, scoring='accuracy', cv=5)
    ret3=scores.mean()

    result=[sg_v,scale,ret1,ret2,ret3]
    print result

    return result


#print test_sentvec(0,0.1)

from sklearn.grid_search import ParameterSampler, ParameterGrid
#params={'sg_v':[0,1],'scale':[2.0**(-n) for n in range(20)]}
#params={'sg_v':[1],'scale':[2.0**(-n) for n in range(20)]}
params={'sg_v':[1],'scale':[2.0**(n+1) for n in range(20)]}
print params
param_list = list(ParameterGrid(params))
print param_list

result=[test_sentvec(**param) for param in param_list]
print result

    ## non shuffle
    # sg_v=0
    # 0.538902704141
    # 0.692475037989
    # 0.537310549242

    # sg_v=1 
    # 0.611053293365
    # 0.697653222928
    # 0.610875989755

    ## shuffled
    # sg_v=0 score 1/10
    # 0.426177333191
    # 0.444867961652
    # 0.431898204423

    # sg_v=1 score 1/100
    # 0.487316849967
    # 0.474215855992
    # 0.487140206225

    # sg_v=1 score 1/500
    # 0.479182138158
    # 0.470971988597
    # 0.479182138158



# [1, 1.0, 0.48743532980102361, 0.49350754275254866, 0.48495790558488017]
# 16964
# [1, 0.5, 0.47924301524751478, 0.48637491503720753, 0.47511290890913116]
# 16964
#[1, 0.25, 0.48218813817300277, 0.48684657689048044, 0.48083085848747642]
# [1, 2.0, 0.48372067147114794, 0.48861381114444152, 0.47994600770741264]
# 16964
# [1, 4.0, 0.48743206331836469, 0.49297451893533867, 0.48554398407042426]
# 16964
# [1, 8.0, 0.48189183232472538, 0.48802259092773193, 0.47929498966706136]
# 16964
# /home/niitsumalocal/src/python/gensim/scoredsentence2vec/word2vec.py:1292: RuntimeWarning: overflow encountered in exp
#   fac = 1.0 / (1.0 + exp(-dot(l1, l2c.T)))  #  propagate hidden -> output
# ^CTraceback (most recent call last):
