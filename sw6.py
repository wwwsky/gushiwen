# -*- utf-8 -*-
"""
@url: https://blog.csdn.net/u014534808
@Author: 码农飞哥
@File: gushiwen_rep.py
@Time: 2021/12/7 07:40
@Desc: 用正则表达式爬取古诗文网站
古诗文网站的地址：
https://www.gushiwen.cn/
"""
import re
import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36'
}

first_url = 'https://so.gushiwen.cn/shiwens/default.aspx'


def get_total_pages():
    resp = requests.get(first_url)
    # 获取总页数
    ret = re.findall(
        r'<div class="pagesright">.*?<span .*?>(.*?)</span>', resp.text, re.DOTALL)
    result = re.search('\d+', ret[0])
    for page_num in range(int(result.group())):
        url = 'https://so.gushiwen.cn/shiwens/default.aspx?page=' + \
            str(page_num)
        parse_page(url)


# 解析页面
def parse_page(url):
    resp = requests.get(url)
    text = resp.text
    # 提取标题 (.*) 进行分组，只提取<b>标签中的内容,默认情况下 .不能匹配\n。加上re.DOTALL 表示.号可以匹配所有，贪婪模式
    # titles = re.findall(r'<div class="cont">.*<b>(.*)</b>', text,re.DOTALL)
    # 非贪婪模式
    titles = re.findall(r'<div class="cont">.*?<b>(.*?)</b>', text, re.DOTALL)
    # 提取作者
    authors = re.findall(
        r'<p class="source">.*?<a .*?>(.*?)</a>', text, re.DOTALL)
    # 提取朝代
    dynastys = re.findall(
        r'<p class="source">.*?<a .*?><a .*?>(.*?)</a>', text, re.DOTALL)
    # 提取诗句
    content_tags = re.findall(
        r'<div class="contson" .*?>(.*?)</div>', text, re.DOTALL)
    contents = []
    for content in content_tags:
        content = re.sub(r'<.*?>+', "", content)
        contents.append(content)
    poems = []

    for value in zip(titles, authors, dynastys, contents):
        # 解包
        title, author, dynasty, content = value
        poems.append(
            {
                "title": title,
                "author": author,
                'dynasty': dynasty,
                'content': content
            }
        )
    print(poems)
    """
    poems=[
        {
            "title": '渔家傲·花底忽闻敲两桨',
            "author":'张三',
            'dynasty':'唐朝',
            'content':'xxxxxx'
        }
          {
            "title": '渔家傲·花底忽闻敲两桨',
            "author":'张三',
            'dynasty':'唐朝',
            'content':'xxxxxx'
        }
    ]
    """


"""
zip 函数
a=['name','age']
b=['张三',18]
c=zip(a,b)
c=[
    ('name','张三'),
    ('age',18)
]
"""

if __name__ == '__main__':
    get_total_pages()
