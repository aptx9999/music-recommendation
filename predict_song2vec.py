import pickle
import gensim

song_dic = pickle.load(open("song.pkl", "rb"))
model_str = "./song2vec.model"
model = gensim.models.Word2Vec.load(model_str)

song_id_list = list(song_dic.keys())[:50]

for song_id in song_id_list:
    result_song_list = model.wv.most_similar(song_id)

    print(song_id, song_dic[song_id])
    print("\n相似歌曲和相似度分别为：")
    for song in result_song_list:
        print("\t", song_dic[song[0]], song[1])

    print("\n")