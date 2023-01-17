# -*- coding:utf-8 -*-
#爬取古诗网站
import requests
import re

#下载数据
def write_data(data):
    with open('诗词.txt','a')as f:
        f.write(data)

for i in range(1,10):
    #目标url地址
    url =  "https://so.gushiwen.org/shiwen/default.aspx?page={}".format(i)
    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    html = requests.get(url ,headers = headers).content.decode('utf-8')
    # print(html)
    p_title = '<p><a style="font-size:18px; line-height:22px; height:22px;" href=".*?" target="_blank"><b>(.*?)</b></a></p>'
    title = re.findall(p_title, html)
    # 提取内容
    p_context = '<div class="contson" id=".*?">(.*?)</div>'
    context = re.findall(p_context, html, re.S)
    #提取年代
    p_years = '<p class="source"><a href=".*?">(.*?)</a>'
    years = re.findall(p_years,html,re.S)
    #提取作者
    p_author = '<p class="source"><a href=".*?">.*?</a><span>：</span><.*?>(.*?)</a>'
    author = re.findall(p_author,html)
    # print(context)
    # print(title)
    # print(years)
    # print(author)
    for j in range(len(title)):
        context[j] = re.sub('<.*?>', '', context[j])
        #'gbk' codec can't encode character '\u4729' ，没有这行会出现报错
        context[j] = re.sub(r'\u4729', '', context[j])
        # print(title[j])
        # print(years[j])
        # print(author[j])
        # print(context[j])
        #写入数据
        write_data(title[j])
        write_data('\n'+ years[j])
        write_data(' :'+ author[j])
        write_data(context[j])
    print('下载第{}页成功'.format(str(i)))