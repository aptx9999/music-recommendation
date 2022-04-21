#coding: utf-8
import json
# noinspection PyUnresolvedReferences
import sys
# noinspection PyUnresolvedReferences
import os
from os import path

def parse_song_line(in_line):
		data = in_line
		name = data['歌单名']
		tags = ",".join(data.get('歌单风格'))
		subscribed_count = data['歌单收藏数']
		if(int(subscribed_count)<100):
			return False
		playlist_id = data['歌单ID']
		song_info = ''
		songs = data['歌单歌曲']
		for song in songs:
			try:
				song_info += "\t"+":::".join([str(song['歌曲id']),song['歌曲名'],song['歌曲作者'],str(song['歌曲时长'])])
			except Exception as e:
				print(e)
				print(song)
				continue
		return name+"##"+tags+"##"+str(playlist_id)+"##"+str(subscribed_count)+song_info

def parse_file(in_file, out_file):
	out = open(out_file, 'w', encoding='utf-8')
	file = os.listdir(in_file)
	for f in file :
		real_url = path.join(in_file, f)
		with open(real_url, encoding='utf-8-sig', errors='ignore') as f:
			origin = json.load(f, strict=False)
		for line in origin:
			if type(line.get('歌单风格')) is type([]) :
				result = parse_song_line(line)
				if(result):
					out.write(result.strip()+"\n")

	out.close()



parse_file("./data", "playlist.txt")