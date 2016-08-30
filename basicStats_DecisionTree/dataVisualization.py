# -*- coding: utf-8 -*-
from __future__ import unicode_literals
'''
DATA VISUALIZATION MODULE

OUTPUT: 
* BAR PLOT OF PROVINCE AND CITY FOR DOGFOOD USERS
* PIE CHART OF GENDER FOR DOGFOOD USERS

Jing Wang 
Aug 13, 2016
JD.com, Beijing
'''
__author__ = 'Jing Wang'
__version__ = '1.0'

import pandas as pd 
import matplotlib.pyplot as plt 
import pickle
import seaborn as sns
import re
import numpy as np


# import plotly api to plot pie chart of gender
import plotly.plotly as py
import plotly.graph_objs as go
import plotly 

# my account on plotly api 
plotly.tools.set_credentials_file(username='santiange', api_key='i5gjeqjdin')

class dataVisualization(object):

	'''read top city or top province'''
	def __init__(self, top):
		self.top = top 

	'''province_frequency visualization'''
	def province(self):
		self.top = 29  # only having 29 provinces data
		province_data = pd.read_csv('new_province_id.csv')
		province_data = province_data[province_data.columns[1:]] # remove index column

		# recoginze format and get out of effective data
		province_data.province_name = province_data.province_name.apply(lambda x: re.findall("\t(.+)\t\t", x)[0])
		province_data.province_name = province_data.province_name.apply(lambda x: unicode(x, 'utf-8'))

		plt.figure(1)
		province_data.frequency[:self.top].plot(kind = 'bar', colormap = 'spring')
		plt.xticks(np.arange(self.top), province_data.province_name[:self.top], fontsize = 10, rotation = 90)
		plt.yticks(fontsize = 12)
		plt.xlabel(u'收货地址省市', fontsize = 15)
		plt.ylabel(u'购买频度', fontsize = 15)
		plt.show()

	def city(self):
		city_data = pd.read_csv('new_city_id.csv')
		city_data = city_data[city_data.columns[1:]]
		city_data.city_name = city_data.city_name.apply(lambda x: unicode(x, 'utf-8'))

		plt.figure(2) 
		city_data.frequency[:self.top].plot(kind = 'bar', colormap = 'Set3')
		plt.xticks(np.arange(self.top), city_data.city_name[:self.top], fontsize = 10, rotation = 90)
		plt.yticks(fontsize = 12)
		plt.xlabel(u'收货地址市区', fontsize = 15)
		plt.ylabel(u'购买频度', fontsize = 15)
		plt.show()


	def county(self):
		pass

	'''member_reg_gender {0: male; 1: female, 2: secret, 3: None}'''
	'''see in https://plot.ly/python'''
	def gender(self):
		gender_df = pickle.load(open('gender.p', 'rb'))
		fig = {
			'data': [
			{
				'values': gender_df.frequency , 
				'labels': gender_df.gender, 
				'domain': {'x': [0.26, 0.74]},
				'name': 'Gender',
				'hoverinfo':'label+percent+name',
				'hole': .4,
				'type': 'pie'
			}],
			"layout": 
			{
				"title":"Gender Distribution",
				"annotations": [
				{
				"font": {
					"size": 20
					},
				"showarrow": False,
				"text": "Gender",
				"x": 0.5,
				"y": 0.5
				}
				]
			}
		}
			
		py.iplot(fig)


