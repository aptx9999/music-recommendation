import pandas as pd
import numpy as np
import tensorflow as tf
import pickle

col_names = ["user", "id", "rate", "st"]
ratings_df = pd.read_csv('suprise_format.txt', sep=',', header=None, names=col_names, engine='python')
col_names2 = ["id", "name", "author", "type"]
music_df = pd.read_csv('suprise_format5.txt', sep=',', header=None, names=col_names2, engine='python')



music_df['musicRow'] = music_df.index
music_df = music_df[['musicRow', 'id', 'name']]
music_df.to_csv('musicProcessed.csv', index=False, header=True, encoding='utf-8')
print(music_df.head())
col_names3 = ["user", "uname"]
playlist_df = pd.read_csv('playlist2.txt', sep='&&&', header=None, names=col_names3, engine='python')
playlist_df['playlistRow'] = playlist_df.index

ratings_df = pd.merge(ratings_df, music_df, on='id')
ratings_df = pd.merge(ratings_df, playlist_df, on='user')
ratings_df = ratings_df[['playlistRow','user', 'musicRow', 'rate']]
ratings_df.to_csv('ratingsProcessed.csv', index = False, header=True, encoding='utf-8')
print(ratings_df.tail())

userNo = ratings_df['playlistRow'].max()+1
musicNo = ratings_df['musicRow'].max()+1
print(userNo)
print(musicNo)

rating = np.zeros((musicNo, userNo))

flag = 0
ratings_df_length = np.shape(ratings_df)[0]

for index, row in ratings_df.iterrows():
    rating[int(row['musicRow']), int(row['playlistRow'])] = row['rate']
    flag += 1
    if flag % 5000 == 0:
        print('processed %d, %d left' % (flag, ratings_df_length-flag))
record = rating>0
record = np.array(record, dtype=int)
print(record)


def normalizeRatings(rating, record):
    m, n = rating.shape
    rating_mean = np.zeros((m, 1))
    rating_norm = np.zeros((m, n))
    for i in range(m):
        idx = record[i, :] !=0
        rating_mean[i] = np.mean(rating[i, idx])
        rating_norm[i, idx] -= rating_mean[i]
    return rating_norm, rating_mean

rating_norm, rating_mean = normalizeRatings(rating, record)
rating_norm = np.nan_to_num(rating_norm)
rating_mean = np.nan_to_num(rating_mean)

num_features = 10
X_parameters = tf.Variable(tf.compat.v1.random_normal([musicNo, num_features], stddev=0.35))
Theta_paramters = tf.Variable(tf.compat.v1.random_normal([userNo, num_features], stddev=0.35))
loss = 1/2 * tf.reduce_sum(((tf.matmul(X_parameters, Theta_paramters, transpose_b=True) - rating_norm)*record)**2) + \
    1/2 * (tf.reduce_sum(X_parameters**2) + tf.reduce_sum(Theta_paramters**2))
optimizer = tf.compat.v1.train.AdamOptimizer()
train = optimizer.minimize(loss)

tf.summary.scalar('loss', loss)
summaryMerged = tf.compat.v1.summary.merge_all()
filename = './music_tensorboard'
writer = tf.compat.v1.summary.FileWriter(filename)
sess = tf.compat.v1.Session()
init = tf.compat.v1.global_variables_initializer()
sess.run(init)

penalty = musicNo*userNo

for i in range(3000):
    l, _, movie_summary = sess.run([loss, train, summaryMerged])
    if i%100 == 0:
        Current_X_parameters, Current_Theta_parameters = sess.run([X_parameters, Theta_paramters])
        predicts = np.dot(Current_X_parameters,Current_Theta_parameters.T) + rating_mean
        errors = np.mean((predicts - rating)**2)
        print('step:', i, ' train loss:%.5f' % (l/penalty), ' test loss:%.5f' % errors)
    writer.add_summary(movie_summary, i)

Current_X_parameters, Current_Theta_parameters = sess.run([X_parameters, Theta_paramters])
predicts = np.dot(Current_X_parameters,Current_Theta_parameters.T) + rating_mean
errors = np.mean((predicts - rating)**2)

print(errors)