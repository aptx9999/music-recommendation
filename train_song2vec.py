#coding: utf-8
import multiprocessing
import gensim
import sys

def parse_playlist_get_sequence(in_line, playlist_sequence):
	song_sequence = []
	contents = in_line.strip().split("\t")
	for song in contents[1:]:
		try:
			song_id, song_name, artist, duration = song.split(":::")
			song_sequence.append(song_id)
		except:
			print("song format error")
			print(song+"\n")
	playlist_sequence.append(song_sequence)


def train_song2vec(in_file, out_file):
	playlist_sequence = []
	with open(in_file, encoding='utf-8-sig', errors='ignore') as f:
		for line in f:
			parse_playlist_get_sequence(line, playlist_sequence)
	cores = multiprocessing.cpu_count()
	print("using all "+str(cores)+" cores")
	print("Training word2vec model...")
	model = gensim.models.Word2Vec(sentences=playlist_sequence, vector_size=150, min_count=3, window=7, workers=cores)
	print("Saving model...")
	model.save(out_file)


song_sequence_file = './playlist.txt'
model_file = './song2vec.model'
train_song2vec(song_sequence_file, model_file)



# def test_song2vec_model(model, song_id):
# 	if __name__ == '__main__':
# 		in_file = sys.argv[1]
# 		out_file = sys.argv[2]
# 		train_song2vec(in_file, out_file)


