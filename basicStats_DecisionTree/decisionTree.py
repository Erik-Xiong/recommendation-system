# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#!usr/bin/python
'''
DECISION TREE METHOD TO TRAIN AND PREDICT

Jing Wang 
Aug 13, 2016
JD.com, Beijing
'''
from __future__ import generators

__author__ = 'Jing Wang'
__version__ = '1.0'

import pandas as pd
import numpy as np
from sklearn import tree
from sklearn import metrics
from sklearn.grid_search import RandomizedSearchCV
import pydot
from os import system

class decisionTree(object):

	def __init__(self):
		self.Xtrain = None 
		self.Ytrain = None
		self.Xtest = None
		self.Ytest = None
		self.data = None
		self.DT = None

	
	def train(self):
		self.DT = tree.DecisionTreeClassifier(criterion = 'entropy', splitter = 'best', random_state = 99,
			max_leaf_nodes = 6) 

		''' cross validation tree, loop different parameters and find the best tree'''
		# param_dis = {"criterion": ["entropy"],
		# 		  "min_samples_split": [2], # (default:2) The minimum number of samples required to split an internal node
		# 		  "max_depth": [30],
		# 		  "min_samples_leaf": [1],
		# 		  "max_leaf_nodes": [None],
		# 		  }
		# random_search = RandomizedSearchCV(self.DT, param_dis, n_iter=1, cv = 6)
		# self.DT = random_search.fit(self.Xtrain,self.Ytrain)

		# self.DT = self.DT.best_estimator_

		'''common tree'''
		self.DT = self.DT.fit(self.Xtrain, self.Ytrain)

	'''output accuracy'''
	def accuracy(self):
		Yhat = self.DT.predict(self.Xtest)

		return np.mean(Yhat == self.Ytest)

	'''tree plotting, output as tree.png file '''
	def plot(self):
		dec_tree = open('tree.dot','w')
		tree.export_graphviz(self.DT, out_file = dec_tree, feature_names = self.data.columns.values, 
			class_names = ['0', '1'], filled = True)

		dec_tree.close()
		system('dot -Tpng tree.dot -o tree.png')


	''' accept feature columns 
	    use_col : feature columns 
	'''
	def getData(self, use_col):
		self.use_col = use_col
		self.data = pd.read_csv('usr_tag.csv', usecols = self.use_col)

	'''train and test partition and accept percent parameter, by default percent = 0.8'''
	def partition(self, percent = 0.8):
		np.random.seed(10)

		'''80% percent dogFood users basket to train'''
		dogFood = self.data[self.data['label'] == 1]
		sample_dogFood = np.random.rand(len(dogFood)) <= percent
		dogFood_train = np.asarray(dogFood[sample_dogFood])
		dogFood_test = np.asarray(dogFood[~sample_dogFood])

		others = self.data[self.data['label'] == 0]

		sample_others = np.random.rand(len(others)) <= len(dogFood[sample_dogFood]) /3. * 7./ float(len(others)) 
		others_train = np.asarray(others[sample_others])
		sample_others2 = np.random.rand(len(others)) <= len(dogFood[~sample_dogFood]) /3. * 7./ float(len(others)) 
		others_test = np.asarray(others[sample_others2])

		'''percentage 30%  dogFood user,  70%  other users to make up train data'''
		train = np.vstack((dogFood_train, others_train))
		
		'''percentage 30%  dogFood user,  70%  other users to make up test data'''
		test = np.vstack((dogFood_test , others_test))
		self.Xtrain = train[:, :-1]
		self.Ytrain = train[:, -1]
		self.Xtest = test[:, :-1]
		self.Ytest = test[:, -1]


