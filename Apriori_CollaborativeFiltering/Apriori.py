# -*- coding: utf-8 -*-
#
# Apriori.py
# --------------
# Attribution Information: The recommendation system projects were developed at JD.com.
# The core projects and autograders were primarily created by Xincheng Xiong
# (xincheng.xiong@gmail.com) and ...

from __future__ import division
from Base import Base
import numpy as np
import operator

class Apriori(Base):
  def __init__(self):
    super().__init__()
    self.name = "Apriori"
    self._confidence = {}
    self._relatives = []
    self._singleSupport = {}
    self._combineSupport = {}

  def fit(self):
    if not self.isDataProcessed:
      raise Exception('data has not been processed')
    if not bool(self._relatives):
      self._relatives = sorted(self.confidence.items(), key=operator.itemgetter(1), reverse = True)
    return self.confidence

  def predict(self, Xdata):
    if not bool(self.confidence):
      raise Exception('the apriori model is untrained')
    temp = np.array(Xdata, dtype=float, copy=True)
    for k, v in self._relatives:
      temp[:, self.itemIndex[k]] *= v
    return np.amax(temp, axis=1)



  @property
  def singleSupport(self):
    if not bool(self._singleSupport):
      ss = np.sum(self.Xtrain, axis=0) #/ self.trainUsrNum
      for k, i in self.itemIndex.items():
        self._singleSupport[k] = ss[i]
    return self._singleSupport

  @property
  def combineSupport(self):
    if not bool(self._combineSupport):
      combinedMatrix = self.Xtrain & self.Ytrain.reshape(len(self.Ytrain), 1)
      cs = np.sum(combinedMatrix, axis=0) #/ self.trainUsrNum
      for k, i in self.itemIndex.items():
        self._combineSupport[k] = cs[i]
    return self._combineSupport
  
  @property
  def confidence(self):
    if not bool(self._combineSupport):
      for k in self.itemIndex.keys():
        self._confidence[k] = self.combineSupport[k] / float(self.singleSupport[k]) if self.singleSupport[k] else 0
    return self._confidence
  
