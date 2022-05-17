
from surprise import KNNWithMeans, Reader, Dataset,accuracy
from surprise.model_selection import cross_validate,KFold
import os

file_path = os.path.expanduser('./suprise_format3.txt')
reader = Reader(line_format='user item rating', sep=',')
music_data = Dataset.load_from_file(file_path, reader=reader)
kf = KFold(n_splits=5)
algo = KNNWithMeans()
perf = cross_validate(algo, music_data, measures=['RMSE', 'MAE'], cv=5, verbose=True)





# from surprise import SVD
# from surprise import Dataset
# from surprise import accuracy
# from surprise.model_selection import KFold
#
# data = Dataset.load_builtin("ml-100k")
# kf = KFold(n_splits=3)
# algo = SVD()
# for trainData, testData in kf.split(data):
#     algo.fit(trainData)
#     predictions = algo.test(testData)
#     accuracy.rmse(predictions, verbose=False)
#
# 同样的，可以使用交叉验证去实现效果
#
# from surprise import SVD
# from surprise import Dataset
# from surprise.model_selection import GridSearchCV
#
# # Use movielens-100K
# data = Dataset.load_builtin('ml-100k')
#
# param_grid = {'n_epochs': [5, 10], 'lr_all': [0.002, 0.005],
#               'reg_all': [0.4, 0.6]}
#
# gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)
# gs.fit(data)
#
# # best RMSE score
# print(gs.best_score['rmse'])
# # combination of parameters that gave the best RMSE score
# print(gs.best_params['rmse'])
#
# # We can now use the algorithm that yields the best rmse:
# algo = gs.best_estimator['rmse']
# algo.fit(data.build_full_trainset())