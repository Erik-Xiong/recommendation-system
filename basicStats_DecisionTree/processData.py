# -*- coding: utf-8 -*-
from __future__ import unicode_literals
'''
DATA PREPROCESS

OUTPUT: 
* NEW DATAFRAME WITH NEW COLUMN "label" 1 FOR DOGFOOD USERS 0 FOR OTHERS WITH FILENAME 'usr_tag.csv’
* province_id.p, city_id.p, county_id.p, THREE FILES. IN ORDER TO OBTAIN THE CORRESPONDING PROVINCE NAMES 
  CITY NAMES, COUNTY NAMES BASED ON TABLES ON JD.COM 
* gender.p FOR DATA VISUALIZATION 


Jing Wang
Aug 13, 2016
JD.com, Beijing

'''
import pandas as pd 
import pickle
from collections import Counter
import numpy as np 

'''read data'''
use_col = ['item_third_cate_cd', 'item_third_cate_name', 'member_reg_gender', 
           'user_id', 'reg_birthday', 'reg_user_type_cd','user_lv_cd', 
           'sale_ord_tm', 'sale_ord_dt','rev_addr_province_id', 
           'rev_addr_city_id', 'rev_addr_county_id']

filename = 'new_data_0818.csv'
data = pd.read_csv(filename, usecols = use_col)

'''obtain dogFood data'''
dogFood_id  = 7002 # dogFood id 
dogFood_data = data[data['item_third_cate_cd']==dogFood_id]


'''Add label data and save it to new data file'''
dogFood_user_list = pd.Series.unique(dogFood_data['user_id']).tolist()
np.random.shuffle(dogFood_user_list)

'''add label column and gender string to float'''
data['label'] = data['user_id'].apply(lambda x: 1 if x in dogFood_user_list else 0)

'''let format be consistent'''
def genderConvert(group):
    try: 
        return int(group)
    except:
        return -1

def userType(group):
    try: 
        return int(group)
    except:
        return -1

data['member_reg_gender'] = data['member_reg_gender'].apply(genderConvert)
data['reg_user_type_cd'] = data['reg_user_type_cd'].apply(userType)

'''save to new file'''
data.to_csv('usr_tag.csv')


################################################################################
'''obtain province_id, city_id, county_id
and related frequency for data visualization'''
def getFreq(data, colname, newColname, filename):
	filtered_data = Counter(data[colname])
	filtered_data_df = pd.DataFrame(filtered_data.items()).rename(columns = {0: newColname, 1: 'frequency'})
	
	# from big to small
	filtered_data_df = filtered_data_df.sort_values(['frequency'], ascending = 0)
	
	pickle.dump(filtered_data_df, open(filename, 'wb'))

'''output province_freq, city_freq, county_id as .p file
in order to get the corresponding province names, city names and county names in terms of ids'''

getFreq(dogFood_data, 'rev_addr_province_id', 'province_id', 'province_id.p')
getFreq(dogFood_data, 'rev_addr_city_id', 'city_id', 'city_id.p')
getFreq(dogFood_data, 'rev_addr_county_id', 'county_id', 'county_id.p')



################################################################################
'''Dealing with gender data， translate to Chinese'''
def genderTrans(group):
	if group == '0' or group == 0:
		return u'男'
	elif group == '1' or group == 1:
		return u'女'
	elif group == '2' or group == 2:
		return u'保密'
	elif group == 'None':
		return u'未填写'

'''translate to Chinese for data visualization'''
dogFood_data['member_reg_gender'] = dogFood_data['member_reg_gender'].apply(genderTrans)
getFreq(dogFood_data, 'member_reg_gender', 'gender', 'gender.p')



