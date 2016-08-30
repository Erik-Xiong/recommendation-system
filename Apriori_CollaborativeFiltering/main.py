# -*- coding: utf-8 -*-
#
# main.py
# --------------
# Attribution Information: The recommendation system projects were developed at JD.com.
# The core projects and autograders were primarily created by Xincheng Xiong
# (xincheng.xiong@gmail.com) and ...

from Apriori import Apriori
from Random_Ads import Random_Ads
from Collaborative_Filtering import CF
import numpy as np
import pickle
import operator

a = Random_Ads()
a.processData()
a.fit()
print(a.benchmark(a.Ytest, a.predict(a.Xtest), 5000000))

b = Apriori()
b.processData()
b.fit()
print(b.benchmark(b.Ytest, b.predict(b.Xtest), 5000000))


c = CF()
c.processData()
c.fit()
c.predict(c.Xtest)
print(c.benchmark(c.Ytest, c.predict(c.Xtest), 5000000))