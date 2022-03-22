import re
import time
import requests
from fake_useragent import UserAgent
from Utils.MySqlConnect import connectDB
from Utils.setting import COOKIE
import json

# 获取被引用文章信息
print("欢迎来到谷歌学术信息获取系统（以作者为搜索核心）。")
print('___________________________________________________')
# 打开数据库连接
db = connectDB()
# 使用cursor()方法获取操作游标
cursor = db.cursor()
# SQL查询并列出学者和ID
sql = "select ID ,Name from scholars"
try:
    cursor.execute(sql)
    result = cursor.fetchall()
    print("编号\t 姓名")
    print('___________________________________________________')
    for row in result:
        ID = row[0]
        Name = row[1]
        print(row[0], "\t", row[1])
    print('___________________________________________________')
except:
    print("数据库连接有误。")

# 选择学者
scholar_id = int(input("请输入学者编号 : "))
# SQL查询学者谷歌学术主页 默认图灵谷歌学术主页
sql = "select Name,GoogleScholarID from scholars where ID = %d" % scholar_id
Name = "Alan Turing"
GoogleScholarID = "VWCHlwkAAAAJ"
try:
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        GoogleScholarID = row[1]
        Name = row[0]
except:
    print("数据库连接有误。")
print('___________________________________________________')
url = "https://scholar.google.com/citations?user=" + GoogleScholarID + "&hl=en&oi=ao"
print(Name, "的谷歌学术主页网址为:")
print(url)
print('___________________________________________________')

# 随机UserAgent
ua = UserAgent().random
# 获取作者文章列表
try:
    requests.packages.urllib3.disable_warnings()
    gs_page = requests.get(url, headers={'User-Agent': ua}, verify=False).text
except requests.exceptions.ConnectionError:
    time.sleep(5)
    print("获取频率过快。")

i = 1
# 论文序号
paper_title_list = []  # 论文标题
paper_cited_times_list = []  # 引用次数
paper_time_list = []  # 年份
paper_url_list = []  # 网址

# 被引用论文
cited_paper_title_list = []  # 论文标题
cited_paper_durl_list = []  # 下载网址
cited_paper_url_list = []  # 论文信息网址

print(Name, "的谷歌学术中引用次数最多的20篇文章:")
print("编号 \t年份\t引用\t\t标题")
print("___________________________________________________")
paper_lists = re.findall(
    r'<tr class="gsc_a_tr"><td class="gsc_a_t">.*?<td class="gsc_a_y"><span class="gsc_a_h gsc_a_hc gs_ibl">.*?</span></td></tr>',
    gs_page, re.I)
for paper_list in paper_lists:
    paper_title = re.findall(r'class="gsc_a_at">(.*?)</a><div class="gs_gray">', paper_list)
    paper_cited = re.findall(r'class="gsc_a_ac gs_ibl">(.*?)</a>', paper_list)
    paper_time = re.findall(r'<span class="gsc_a_h gsc_a_hc gs_ibl">(.*?)</span>', paper_list)
    paper_url = re.findall(r'<a href="(.*?)" class="gsc_a_at">', paper_list)
    if len(paper_title):
        paper_title = paper_title[0]
        paper_title = paper_title.replace("<i>", "")
        paper_title = paper_title.replace("</i>", "")
    if len(paper_cited):
        paper_cited = paper_cited[0]
    if len(paper_time):
        paper_time = paper_time[0]
    if len(paper_url):
        paper_url = paper_url[0]
    paper_url = paper_url.replace('&amp;', '&')
    paper_url = "https://scholar.google.com" + paper_url

    # 存储数据
    paper_title_list.append(paper_title)
    paper_cited_times_list.append(paper_cited)
    paper_time_list.append(paper_time)
    paper_url_list.append(paper_url)

    print(i, "\t ", paper_time, "\t", paper_cited, "\t", paper_title)
    print("URL: ", paper_url)
    print('___________________________________________________')
    i = i + 1
isQuit = 1
isOneRun = 0
while isQuit:
    print("0.退出系统")
    print("1.引用论文列表")
    print("2.论文与其作者信息")
    print("3.下载论文")
    print('___________________________________________________')
    funcNum = int(input("请输入你想要的功能编号: "))
    if funcNum == 0:
        isQuit = 0
        print("退出系统，再见！")
        print('___________________________________________________')
        break
    if funcNum == 1:
        paper_id = int(input("请输入论文编号: "))
        print('___________________________________________________')
        print("标题: ", paper_title_list[paper_id - 1])
        ua = UserAgent().random
        try:
            requests.packages.urllib3.disable_warnings()
            paper_page = requests.get(paper_url_list[paper_id - 1],
                                      headers={'User-Agent': ua}, verify=False).text
        except requests.exceptions.ConnectionError:
            time.sleep(5)
            print("获取频率过快。")
        str = '<div class="gsc_oci_merged_snippet"><div><a href="(.*?)">' + paper_title_list[paper_id - 1]
        paper_url = re.findall(r'' + str, paper_page, re.I)[0]
        paper_url = paper_url.replace('&amp;', '&')
        paper_url = "https://scholar.google.com" + paper_url
        print("论文网址:", paper_url)
        str = '<div class="gsc_oci_value"><div style="margin-bottom:1em"><a href="(.*?)">Cited'
        cited_list_url = re.findall(r'' + str, paper_page, re.I)[0]
        cited_list_url = cited_list_url.replace('&amp;', '&')
        print("引用论文页面网址:" + cited_list_url)
        print('___________________________________________________')
        ua = UserAgent().random
        try:
            requests.packages.urllib3.disable_warnings()
            cited_list_page = requests.get(cited_list_url,
                                           headers={
                                               'User-Agent': ua,
                                               'Cookie': COOKIE}).text
        except requests.exceptions.ConnectionError:
            time.sleep(5)
            print("请求频率过快。")
        cited_list = re.findall(
            r'<div class="gs_r gs_or gs_scl".*?</div></div></div>  '
            r'|<div class="gs_r gs_or gs_scl".*?</div></div></div></div>+',
            cited_list_page, re.I)
        if len(cited_list) == 0:
            print("\033[0;31m%s\033[0m" % "获取失败，请稍后再试。")
            print('___________________________________________________')
        else:
            i = 1
            for cited in cited_list:
                # 论文编号，需要存储
                data_id = re.findall(r'<div class="gs_r gs_or gs_scl" data-cid="(.*?)" data-did', cited)[0]
                cited_title_text = re.findall(r'<a id=.*?</a></h3>', cited)[0]
                cited_title = re.findall(r'>(.*?)</a></h3>', cited_title_text)[0]
                cited_url = re.findall(r'href="(.*?)" d', cited_title_text)[0]
                cited_paper_pdf_durl = re.findall(r'<a href="(.*?)" data-clk=', cited)
                if len(cited_paper_pdf_durl) == 0:
                    url_str = ""
                else:
                    url_str = cited_paper_pdf_durl[0]
                print(i, "\t", cited_title)
                print("论文下载网址:", url_str)
                print('___________________________________________________')
                i = i + 1
                # 保存信息
                cited_paper_title_list.append(cited_title)
                cited_paper_durl_list.append(url_str)
                cited_paper_url_list.append(cited_url)
                isOneRun = 1

    if funcNum == 2:
        if isOneRun == 1:
            paper_id = int(input("请输入引用论文编号: "))
            print('___________________________________________________')
            if paper_id > len(cited_paper_title_list):
                paper_id = len(cited_paper_title_list) - 1
            print(cited_paper_title_list[paper_id - 1])
            print("URL:", cited_paper_url_list[paper_id - 1])
            print('___________________________________________________')
            ua = UserAgent().random
            # xplore 网站
            if 'ieeexplore.ieee.org' in cited_paper_url_list[paper_id - 1]:
                try:
                    requests.packages.urllib3.disable_warnings()
                    cited_page = requests.get(cited_paper_url_list[paper_id - 1],
                                              headers={'User-Agent': ua}).text
                except requests.exceptions.ConnectionError:
                    time.sleep(5)
                    print("获取频率过快。")
                info_text = re.findall(r'xplGlobal.document.metadata.*?};', cited_page)[0]
                info_text = info_text.replace("xplGlobal.document.metadata=", "")
                info_text = info_text[:-1]
                info = json.loads(info_text)
                if 'publisher' in info.keys():
                    print("发布:", info['publisher'])
                if 'publicationYear' in info.keys():
                    print("年份:", info['publicationYear'])
                if 'citationCount' in info.keys():
                    print("被引用次数:", info['citationCount'])
                if 'abstract' in info.keys():
                    print("摘要:", info['abstract'])
                if 'authors' in info.keys():
                    print("作者:", end=" ")
                    i = 1
                    for author in info['authors']:
                        print(author['name'], i, end='\t')
                        i = i + 1
                    print('\n___________________________________________________')
                    isAuthorQuit = 1
                    while isAuthorQuit:
                        author_id = int(input("如需获取作者详细信息，请输入编号,否则输入0退出:"))
                        if author_id == 0:
                            isAuthorQuit = 0
                            break
                        if author_id > i:
                            author_id = i
                        print("姓名:", info['authors'][author_id - 1]['name'])
                        if 'affiliation' in info['authors'][author_id - 1]:
                            print("单位:", info['authors'][author_id - 1]['affiliation'][0])
                        if 'id' in info['authors'][author_id - 1]:
                            print("个人主页(Xplore):",
                                  'https://ieeexplore.ieee.org/author/' + info['authors'][author_id - 1]['id'])
                        if 'bio' in info['authors'][author_id - 1]:
                            print("简介:", info['authors'][author_id - 1]['bio']['p'][0])
                        print('___________________________________________________')
                print('___________________________________________________')
            else:
                print("除了xplore，其他网页正在实现中....")
                print('___________________________________________________')
        else:
            print("请选运行功能1，获取引用论文列表。")
            print('___________________________________________________')

    if funcNum == 3:
        print("功能正在实现中...")
        print('___________________________________________________')

    if funcNum > 3:
        print("输入序号错误。")
        print('___________________________________________________')
