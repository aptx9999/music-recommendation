# coding: utf-8
import sys
import pickle as pk

def parse_playlist_get_info(in_line, playlist_dic, song_dic):
    contents = in_line.strip().split("\t")
    name, tags, playlist_id, subscribed_count = contents[0].split("##")
    playlist_dic[playlist_id] = name
    for song in contents[1:]:
        try:
            song_id, song_name, artist, duration = song.split(":::")
            song_dic[song_id] = song_name + "\t" + artist
        except:
            print
            "song format error"
            print
            song + "\n"


def parse_file(in_file, out_playlist, out_song):
    # 从歌单id到歌单名称的映射字典
    playlist_dic = {}
    # 从歌曲id到歌曲名称的映射字典
    song_dic = {}
    with open(in_file, encoding='utf-8-sig', errors='ignore') as f:
        for line in f:
            parse_playlist_get_info(line, playlist_dic, song_dic)
    # 把映射字典保存在二进制文件中
    pk.dump(playlist_dic, open(out_playlist, "wb"))
    # 可以通过 playlist_dic = pickle.load(open("playlist.pkl","rb"))重新载入
    pk.dump(song_dic, open(out_song, "wb"))


parse_file("./playlist.txt", "playlist.pkl", "song.pkl")