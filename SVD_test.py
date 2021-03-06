from __future__ import (absolute_import, division, print_function, unicode_literals)
import os
import io
from surprise import KNNBaseline, Reader
from surprise import Dataset

def read_item_names():
    file_name = (os.path.expanduser('~') +
                 'u.item')
    rid_to_name = {}
    name_to_rid = {}
    with io.open(file_name, 'r', encoding = 'ISO-8859-1') as f:
        for line in f:
            line = line.split('|')
            rid_to_name[line[0]] = line[1]
            name_to_rid[line[1]] = line[0]
        return rid_to_name, name_to_rid

#首先，用算法计算相互间的相似度
data = Dataset.load_builtin('ml-100k')
trainset = data.build_full_trainset()
sim_options = {'name':'pearson_baseline','user_based':False}
algo = KNNBaseline(sim_options=sim_options)
algo.train(trainset)

#获取电影名到电影id 和 电影id到电影名的映射
rid_to_name, name_to_rid = read_item_names()

#拿出来Toy Story这部电影对应的item idy
toy_story_raw_id = name_to_rid['Toy Story (1995)']
toy_story_inner_id = algo.trainset.to_inner_iid(toy_story_raw_id)

#找到最近的10个邻居
toy_story_neighbors = algo.get_neighbors(toy_story_inner_id, k=10)
toy_story_neighbors = (algo.trainset.to_raw_iid(inner_id)
                       for inner_id in toy_story_neighbors)
toy_story_neighbors = (rid_to_name[rid]
                       for rid in toy_story_neighbors)

print()
print('The 10 nearest neighbors of Toy Story are:')
for movie in toy_story_neighbors:
    print(movie)