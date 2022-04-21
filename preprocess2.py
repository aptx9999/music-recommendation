# coding: utf-8
# noinspection PyUnresolvedReferences
import json
# noinspection PyUnresolvedReferences
import sys


def is_null(s):
    return len(s.split(",")) > 2


def parse_song_info(song_info):
    try:
        song_id, name, artist, duration = song_info.split(":::")
        # return ",".join([song_id, name, artist, popularity])
        return ",".join([song_id, "1.0"])
    except Exception as e:
        # print e
        # print song_info
        return ""


def parse_playlist_line(in_line):
    try:
        contents = in_line.strip().split("\t")
        name, tags, playlist_id, subscribed_count = contents[0].split("##")
        songs_info = map(lambda x: playlist_id + "," + parse_song_info(x), contents[1:])
        songs_info = filter(is_null, songs_info)
        return "\n".join(songs_info)
    except Exception as e:
        print(e)

        return False


def parse_file(in_file, out_file):
    out = open(out_file, 'w',encoding='utf-8')
    with open(in_file, encoding='utf-8-sig', errors='ignore') as f:
        for line in f:
            result = parse_playlist_line(line)
            if (result):
                out.write(result.strip() + "\n")
    out.close()

parse_file("./playlist.txt", "./suprise_format.txt")