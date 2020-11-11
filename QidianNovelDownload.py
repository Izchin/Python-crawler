#!/usr/bin/python
# -*- coding:utf-8 -*-
# Time : 2019/8/22

import requests
import re

url = input(print("本程序可用于下载起点小说，请输入小说主目录页网址："))
# 注意：这程序只能一次下载一个小说。
response = requests.get(url)
response.encoding = 'utf-8'
# 下载一部小说
html = response.text
title = re.findall(r'<meta name="keywords" content="(.*?)">', html)[0]
print(title)
fb = open('%s.txt' % title, 'w', encoding='utf-8')
d1 = re.findall(r'<ul class="cf">.*?</ul>', html, re.S)[0]
chapter_info_list = re.findall(r'<li data-rid="(.*?)"><a href="//(.*?)'
                               r'" target="_blank" data-eid="qd_G55" data-cid="//(.*?)'
                               r'" title="(.*?)">(.*?)</a>', d1)

for chapter_info in chapter_info_list:
    chapter_url = chapter_info[1]
    chapter_title = chapter_info[4]
    chapter_url = "https://%s" % chapter_url

    chapter_response = requests.get(chapter_url)
    chapter_response.encoding = 'utf-8'
    chapter_html = chapter_response.text
    chapter_content = re.findall(r'<div class="read-content j_readContent">(.*?)</div>', chapter_html, re.S)[0]
    chapter_content = chapter_content.replace(' ', '')
    chapter_content = chapter_content.replace('<p>', '\n')
    fb.write(chapter_title)
    fb.write(chapter_content)
    fb.write('\n')
    print(chapter_title, '正在下载中...')

print('《%s》已下载完毕！' % title)
