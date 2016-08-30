# -*- coding: utf-8 -*-

# preprocess.py
# --------------
# Attribution Information: The recommendation system projects were developed at JD.com.
# The core projects and autograders were primarily created by Xincheng Xiong
# (xincheng.xiong@gmail.com) and ...

import pandas as pd
import numpy as np
import pickle
import h5py

full_colnames = ['brandname',
                 'item_first_cate_cd',
                 'item_first_cate_name',
                 'item_second_cate_cd',
                 'item_second_cate_name',
                 'item_third_cate_cd',
                 'item_third_cate_name',
                 'sale_ord_det_id',
                 'sale_ord_id',
                 'parent_sale_ord_id',
                 'sale_ord_type_cd',
                 'sale_ord_cate_cd',
                 'user_id',
                 'sale_ord_tm',
                 'sale_ord_dt',
                 'sale_ord_det_tm',
                 'out_wh_tm',
                 'ord_complete_tm',
                 'dt',
                 'item_sku_id',
                 'item_id',
                 'item_name']

use_colnames = ['brandname',
                'item_first_cate_cd',
                'item_first_cate_name',
                'item_second_cate_cd',
                'item_second_cate_name',
                'item_third_cate_cd',
                'item_third_cate_name',
                'user_id'
                ]
# # save partial data.

data = pd.read_csv('whole.csv', usecols=use_colnames, error_bad_lines=False, low_memory=False)
data.to_csv('part_data.csv', encoding='utf-8')

# read partial data.
data = pd.read_csv('part_data.csv', encoding='utf-8', low_memory=False)

# # save third category id to name dictionary

third_cate_name = data[['item_third_cate_cd', 'item_third_cate_name']].drop_duplicates(subset='item_third_cate_cd', keep='first').sort_values(by='item_third_cate_cd')
third_cate_name.to_csv('third_cate_id_to_name.csv', index=False, encoding='utf-8')
dic_id_to_name = dict(zip(third_cate_name.item_third_cate_cd, third_cate_name.item_third_cate_name))
pickle.dump(dic_id_to_name, open("third_cate_id_to_name.p", "wb"))

item_third_list = pd.Series.unique(data['item_third_cate_cd']).tolist()
item_third_list = sorted(item_third_list)

# move 狗粮 to the front
item_third_list.remove(7002)
item_third_list.remove(7004)
item_third_list.remove(7007)
item_third_list.remove(7016)
item_third_list.insert(0, 7002)

# # move 巧克力 to the front
# item_third_list.remove(1594)
# item_third_list.remove(5021)
# item_third_list.insert(0, 1594)

# shuffle the rows
user_id_list = pd.Series.unique(data['user_id']).tolist()
np.random.shuffle(user_id_list)

# save id_index_matching dictionary.
dic_item_to_index = {k: v for (v, k) in enumerate(item_third_list)}
dic_usr_to_index = {k: v for (v, k) in enumerate(user_id_list)}

# construct userID to itemID matrix
matrix = np.zeros((len(user_id_list), len(item_third_list)), dtype=np.uint8)

# fill the matrix.
ratings = [] # for collaborative filtering
for _, pair in data[['user_id','item_third_cate_cd']].iterrows():
    if pair[1] in [7004, 7007, 7016]:
    # if pair[1] in [5021]:
        if matrix[dic_usr_to_index[pair[0]], 0] == 0:
            matrix[dic_usr_to_index[pair[0]], 0] = 1
            ratings.append((dic_usr_to_index[pair[0]], 0, 1))
    else:
        if matrix[dic_usr_to_index[pair[0]], dic_item_to_index[pair[1]]] == 0:
            matrix[dic_usr_to_index[pair[0]], dic_item_to_index[pair[1]]] = 1
            ratings.append((dic_usr_to_index[pair[0]], dic_item_to_index[pair[1]], 1))

# delete label index, update item index dictionary
del item_third_list[0]
dic_item_to_index = {k: v for (v, k) in enumerate(item_third_list)}

# save the matrix and index dictionary.
# with h5py.File('data.h5', 'w') as hf:
#     hf.create_dataset('matrix', data=matrix)

pickle.dump(dic_item_to_index, open("data/dic_item_to_index.p", "wb"))
pickle.dump(dic_usr_to_index, open("data/dic_usr_to_index.p", "wb"))
np.save('data/matrix.npy', matrix)
np.save('data/ratings.npy',np.array(ratings))

