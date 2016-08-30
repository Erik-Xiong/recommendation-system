# -*- coding: utf-8 -*-
#
# Collaborative_Filtering.py
# --------------
# Attribution Information: The recommendation system projects were developed at JD.com.
# The core projects and autograders were primarily created by Xincheng Xiong
# (xincheng.xiong@gmail.com) and ...

from __future__ import division
from Base import Base
from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
from math import sqrt
from operator import add
import numpy as np
import sys
import itertools
import pickle

class CF(Base):
  def __init__(self):
    super().__init__()
    self.name = "Collaborative filtering"
    self.finalModel = None
    self.finalRank  = 0
    self.finalRegul = float(0)
    self.finalIter  = -1
    self.sc = None

  def fit(self):
    ranks  = [5,10,15,20]
    reguls = [0.1,1,10]
    iters  = [5,10,20]
    finalDist = float(100)

    self.sc = SparkContext()
    ratings = np.load("data/ratings.npy").tolist()
    print(ratings[i][3] for i in range(10))
    ratings = self.sc.parallelize(ratings)

    for cRank, cRegul, cIter in itertools.product(ranks, reguls, iters):
      model = ALS.train(ratings, cRank, cIter, float(cRegul))
      dist = self.howFarAreWe(model, ratings, ratings.count())
      if dist < finalDist:
        print("Best so far:%f" % dist)
        self.finalModel = model
        self.finalRank  = cRank
        self.finalRegul = cRegul
        self.finalIter  = cIter
        finalDist = dist
    print(self.finalRank, self.finalRegul, self.finalIter)

  def predict(self, Xdata):
    print('Collaborative filtering prediction takes existed positive labels as training part, so here we train entire data, and give a rating to each user as their potentials to buy the product.')
    indices = [(i, 0) for i in range(self.data.shape[0])]
    indices = self.sc.parallelize(indices)
    ratings = self.finalModel.predictAll(indices)
    ratings = ratings.map(lambda r: r[2]).collect()
    np.save('temp.npy', ratings)
    return ratings



  def howFarAreWe(self, model, against, sizeAgainst): 
    againstNoRatings = against.map(lambda x: (int(x[0]), int(x[1])) )
    againstWiRatings = against.map(lambda x: ((int(x[0]),int(x[1])), int(x[2])) )
    predictions = model.predictAll(againstNoRatings).map(lambda p: ( (p[0],p[1]), p[2]) )
    predictionsAndRatings = predictions.join(againstWiRatings).values()
    return sqrt(predictionsAndRatings.map(lambda s: (s[0] - s[1]) ** 2).reduce(add) / float(sizeAgainst))
