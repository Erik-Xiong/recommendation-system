# -*- coding: utf-8 -*-
from __future__ import unicode_literals


'''DATA VISUALIZATION'''
from dataVisualization import dataVisualization

top = 50
pic = dataVisualization(top)
pic.province()
pic.city()
pic.gender()



'''DECISION TREE'''
from decisionTree import decisionTree

# feature columns
use_col = ['member_reg_gender', 'reg_user_type_cd', 'user_lv_cd', 'rev_addr_province_id',
        'rev_addr_city_id', 'rev_addr_county_id', 'label']

model = decisionTree()
model.getData(use_col)
model.partition(0.8)
model.train()
print '''Accuracy: ''', model.accuracy()
model.plot()



