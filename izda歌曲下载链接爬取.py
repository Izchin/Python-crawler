#!/usr/bin/python
# -*- coding:utf-8 -*-

# by izchin
# github : izchin
# Gmail : izchinmt@gmail.com
# Time : 2019/8/23
# 本程序用于搜索izda网站收藏的歌曲，可显示歌曲下载地址！

import re
import requests

# 请注意：请把歌手名和姓分开输入，也可通过歌名来搜索！
singer_first_name = input(print('请输入歌名：'))
singer_last_name = input(print('请输入歌手的姓：'))
url = "http://music.izda.com/?a=search&q=%s+%s" % (singer_last_name, singer_first_name)
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                        ' AppleWebKit/537.36 (KHTML, like Gecko)'
                        ' Chrome/76.0.3809.100 Safari/537.36'}
response = requests.get(url, headers=header)
response.encoding = 'uft-8'
html = response.text
song_html = re.findall(r'<div class="down">چۈشۈرۈش</div>.*?ھەممىنى تاللاش', html, re.S)[0]

song_code_list = re.findall(r'album\"><a href=\"/\?a=player&tid=(.*?)F&q=%D8', html, re.S)

print('歌手：%s %s '% (singer_first_name, singer_last_name))
song_num = 1
for song_url in song_code_list:
    url = 'http://music.izda.com/?a=player&tid=%sF&q=%s+%s' % (song_url, singer_last_name, singer_first_name)
    response_1 = requests.get(url)
    response_1.encoding = 'utf-8'
    html_1 = response_1.text
    song_name = re.findall(r'<font color=\"#3d6699\">(.*?)</font></div>', html_1)
    song_num += 1
    down_url = 'http://music.izda.com/?a=download&tid=%sF&q=%s+%s' % (song_url, singer_last_name, singer_first_name)
    response_2 = requests.get(down_url)
    response_2.encoding = 'utf-8'
    html_2 = response_2.text
    song_down = re.findall(r'value="(.*?)" name="', html_2)
    song_down_url = song_down[0]
    song_down_url = song_down_url.replace(' ', '%20')
    print('第', song_num, '首', ': ', song_name, '  ', song_down_url)
print("已完毕！可直接点击链接进行相关歌曲下载！")



