import pickle
import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
import time
import json
import random
# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# driver=webdriver.Chrome(executable_path ='e:/chromedriver.exe')
# driver.get('http://www.kuwo.cn/playlist_detail/3317482398')
# ele=driver.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div/div[1]/div[2]/div[1]/div[3]/ul/li[2]')
#
#
# ele2=ele.click()
#
# print(ele2)
# time.sleep(10)



count=2400
result=[]
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'}
url="http://www.kuwo.cn/playlists"
response=requests.get(headers=headers,url=url)
if response.status_code == 200:
    print(response.cookies.values()[0])
for k in range(152,450):
    if(k%30==1):
        with open('d:\\data'+str(k)+'.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(result, indent=2, ensure_ascii=False))
            result=[]

    headers2={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
             'cookie': 'kw_token='+response.cookies.values()[0],
             'csrf': response.cookies.values()[0],
    }
    url='http://www.kuwo.cn/api/www/classify/playlist/getRcmPlayList?pn='+str(k+1)
    response = requests.get(headers=headers2, url=url)
    if(response.content):
        r=json.loads(response.text)
    else:
        print('1111111111111')
    one = {}
    for i in range(0,20):
        # print(r)
        count=count+1
        print(count)
        one = {}
        playlist_id=r['data']['data'][i]['id']
        print("歌单ID:" + playlist_id)
        one['歌单ID']=playlist_id
        playlist_url="http://www.kuwo.cn/playlist_detail/"+playlist_id
        response_playlist = requests.get(headers=headers, url=playlist_url)
        html_playlist = response_playlist.text
        soup_playlist = BeautifulSoup(html_playlist, 'html.parser')
        playlist_name=r['data']['data'][i]['name']
        # print("歌单名:" + playlist_name)
        one['歌单名'] = playlist_name
        playlist_author=r['data']['data'][i]['uname']
        # print("歌单作者:" + playlist_author)
        one['歌单作者'] = playlist_author
        try:
            playlist_type = soup_playlist.select('p.type')[0].get_text().split(',')
        except IndexError:
            print("Error: list index out of range")
        else:
        # print("歌单风格：")
        # print(playlist_type)
            one['歌单风格'] = playlist_type
        playlist_total=r['data']['data'][i]['total']
        one['歌单歌曲数']=playlist_total
        playlist_fav=r['data']['data'][i]['favorcnt']
        one['歌单收藏数']=playlist_fav
        try:
            playlist_introduction = soup_playlist.select('p.intr_txt')[0].get_text().replace("\n","").replace(" ","")
        # print("歌单简介:" + playlist_introduction)
        except IndexError:
            print("Error: list index out of range")
        else:
            one['歌单简介'] = playlist_introduction
        musiclist=[]
        for j in range(len(soup_playlist.select('div.song_name.flex_c>a'))):
            music={}
            playlist_musicid = soup_playlist.select('div.song_name.flex_c>a')[j]['href'].replace("/play_detail/", "")
            # print("歌单歌曲id:" + playlist_musicid)
            music['歌曲id']=playlist_musicid
            music_name = soup_playlist.select('div.song_name.flex_c>a')[j].get_text()
            # print("歌曲名:" + music_name)
            music['歌曲名'] = music_name
            music_author=soup_playlist.select('div.song_artist>span')[j].get_text()
            # print("歌曲作者:" + music_author)
            music['歌曲作者'] = music_author
            music_time = soup_playlist.select('div.song_time>span')[j].get_text()
            # print("歌曲时长:" + music_time)
            music['歌曲时长'] = music_time
            musiclist.append(music)

        time.sleep(3.5+random.randint(0,200)/100)
        one['歌单歌曲'] = musiclist
        result.append(one)

    # html=response.text
    # soup=BeautifulSoup(html,'html.parser')
    # ids=soup.select('div.item.item>p>span')
    # ids2=soup.select(('script'))
    #
    # pattern = re.compile(',id:"[0-9]+"')
    #
    # l1=re.findall(pattern, str(ids2), flags=0)
    #
    # one={}
    #
    # for i in range(1):#30
    #
    #     one={}
    #     playlist_id=(l1[i]).replace('\"','').replace(':','').replace(',id','')
    #     print("歌单ID:" + playlist_id)
    #     one['歌单ID']=playlist_id
    #     playlist_url="http://www.kuwo.cn/playlist_detail/"+playlist_id
    #     response_playlist = requests.get(headers=headers, url=playlist_url)
    #     html_playlist = response_playlist.text
    #     soup_playlist = BeautifulSoup(html_playlist, 'html.parser')
    #     playlist_name=soup_playlist.select('h1')[0].get_text()
    #     # print("歌单名:" + playlist_name)
    #     one['歌单名'] = playlist_name
    #     playlist_author=soup_playlist.select('p.artist_name.flex_c>span')[0].get_text()
    #     # print("歌单作者:" + playlist_author)
    #     one['歌单作者'] = playlist_author
    #     playlist_type = soup_playlist.select('p.type')[0].get_text().split(',')
    #     # print("歌单风格：")
    #     # print(playlist_type)
    #     one['歌单风格'] = playlist_type
    #     playlist_introduction = soup_playlist.select('p.intr_txt')[0].get_text().replace("\n","").replace(" ","")
    #     # print("歌单简介:" + playlist_introduction)
    #     one['歌单简介'] = playlist_introduction
    #     musiclist=[]
    #     for j in range(len(soup_playlist.select('div.song_name.flex_c>a'))):
    #         music={}
    #         playlist_musicid = soup_playlist.select('div.song_name.flex_c>a')[j]['href'].replace("/play_detail/", "")
    #         # print("歌单歌曲id:" + playlist_musicid)
    #         music['歌曲id']=playlist_musicid
    #         music_name = soup_playlist.select('div.song_name.flex_c>a')[j].get_text()
    #         # print("歌曲名:" + music_name)
    #         music['歌曲名'] = music_name
    #         music_author=soup_playlist.select('div.song_artist>span')[j].get_text()
    #         # print("歌曲作者:" + music_author)
    #         music['歌曲作者'] = music_author
    #         music_time = soup_playlist.select('div.song_time>span')[j].get_text()
    #         # print("歌曲时长:" + music_time)
    #         music['歌曲时长'] = music_time
    #         musiclist.append(music)
    #     time.sleep(1)
    #     one['歌单歌曲'] = musiclist
    # result.append(one)

with open('d:\\data.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(result, indent=2, ensure_ascii=False))









