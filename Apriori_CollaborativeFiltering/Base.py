# -*- coding: utf-8 -*-
#
# Engine.py
# --------------
# Attribution Information: The recommendation system projects were developed at JD.com.
# The core projects and autograders were primarily created by Xincheng Xiong
# (xincheng.xiong@gmail.com) and ...

import pandas
import inspect
import pickle
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from sklearn import metrics
from abc import abstractmethod
from util import *

class Base():
  def __init__(self):
    self.itemIndex = None
    self.usrIndex = None
    self.itemNum = None
    self.trainUsrNum = None
    self.testUsrNum = None
    self.Xtrain = None  # purchased items
    self.Ytrain = None  # user id and labels
    self.Xtest = None
    self.Ytest = None
    self._processed = False

  def processData(self):
    self.data = np.load("data/matrix.npy")
    self.itemIndex = pickle.load(open( "data/dic_item_to_index.p", "rb" ))
    self.usrIndex = pickle.load(open( "data/dic_usr_to_index.p", "rb" ))
    testData, trainData = partition(data, 10)
    self.Xtrain = np.delete(trainData, 0, 1) # usr id & label
    self.itemNum = self.Xtrain.shape[1]
    self.trainUsrNum = self.Xtrain.shape[0]
    self.Ytrain = trainData[:, 0]

    self.Xtest = np.delete(testData, 0, 1)
    self.testUsrNum = self.Xtest.shape[0]
    self.Ytest = testData[:, 0]
    self._processed = True
  @abstractmethod
  def fit(self):
    """ 
    tune the parameters and save in self attributes.
    """
    raiseNotDefined()


  @abstractmethod
  def predict(self, Xdata):
    """
    using weights to calculate data to predicted labels.
    """
    raiseNotDefined()
    
  def crossValidation(self, k):
    n = self.Xtrain.shape[0]
    step = n//10
    losses = []
    for i in range(10):
      Xv = Xtrain[step*i:step*(i+1)]
      Yv = Ytrain[step*i:step*(i+1)]
      Xt = np.vstack((self.Xtrain[0:step*i], self.Xtrain[step*(i+1):]))
      Yt = np.hstack((self.Ytrain[0:step*i], self.Ytrain[step*(i+1):]))
      self.fit(Xv, Yv)
      Ypredict = self.predict(Xt)
      rmse = sqrt(metrics.mean_squared_error(Yt, Ypredict))
    losses.append(rmse)
    return np.mean(losses)

  def benchmark(self, Ytrue, Ypredict, adsNum):
    adsNum = int(len(self.usrIndex)*adsNum/170000000) # total # of user in JD
    precision, recall, threshold = metrics.precision_recall_curve(Ytrue, Ypredict)
    average_precision = metrics.average_precision_score(Ytrue, Ypredict)
    plt.clf()
    plt.plot(recall, precision, label=self.name)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title('Precision-Recall: AUC={0:0.2f}'.format(average_precision))
    plt.legend(loc="lower left")
    plt.savefig('plots/{} precision-recall curve.png'.format(self.name), bbox_inches='tight')

    adsQuantity = np.array([(Ypredict >= t).sum() for t in threshold][::-1])
    plt.clf()
    plt.plot(adsQuantity, precision[-2::-1], label=self.name)
    plt.xlabel('Ads quantity')
    plt.ylabel('Precision')
    plt.ylim([0.0, 0.5])
    plt.xlim([0, adsNum])
    plt.title('Precision-Ads Quantity')
    plt.legend(loc="lower left")
    plt.savefig('plots/{} precision-Ads Quantity curve.png'.format(self.name), bbox_inches='tight')

    return np.take(Ytrue, np.argsort(Ypredict)[:-adsNum]).sum() / float(adsNum)

  def isDataProcessed(self):
    return self._processed



 
