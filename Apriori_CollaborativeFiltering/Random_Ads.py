# -*- coding: utf-8 -*-
#
# randomize.py
# --------------
# Attribution Information: The recommendation system projects were developed at JD.com.
# The core projects and autograders were primarily created by Xincheng Xiong
# (xincheng.xiong@gmail.com) and ...

from __future__ import division
from Base import Base
import numpy as np

class Random_Ads(Base):
  def __init__(self):
    super().__init__()
    self.name = 'Random Advertising'

  def fit(self):
    return

  def predict(self, Xdata):
    return np.random.random_sample(len(Xdata))