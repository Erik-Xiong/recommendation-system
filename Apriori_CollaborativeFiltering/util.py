# -*- coding: utf-8 -*-

# util.py
# --------------
# Attribution Information: The recommendation system projects were developed at JD.com.
# The core projects and autograders were primarily created by Xincheng Xiong
# (xincheng.xiong@gmail.com) and ...

import numpy as np

def partition(data, k):
  '''shuffle and partition data to training and testing dataset'''
  np.random.shuffle(data)
  n = data.shape[0]//k
  return data[:n], data[n:]

def raiseNotDefined():
  fileName = inspect.stack()[1][1]
  line = inspect.stack()[1][2]
  method = inspect.stack()[1][3]

  print("*** Method not implemented: %s at line %s of %s" % (method, line, fileName))
  sys.exit(1)

def binarize(values, threshold):
  r = np.copy(values)
  r[r>=threshold] = 1
  r[r<threshold] = 0
  return r

