import requests
from lxml import etree
import re
import os
import time
import xlwt

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
    # 'referer': 'https://dytt8.net/html/gndy/dyzz/list_23_2.html'
}
BASE_DOMIN = 'https://www.gushiwen.cn/default_1.aspx'
def parse_page(url):
    response = requests.get(url, headers=headers)
    text = response.text
    titles = re.findall(r'<b>(.*?)</b>', text, flags=re.DOTALL)  #  flags=re.DOTALL 来对这些 tab, new line 不敏感.
    authors=re.findall(r'<p class="source">.*?<a.*?>(.*?)</a>', text, flags=re.DOTALL)
    dynasty=re.findall(r'<p class="source">.*?<a.*?<a.*?>(.*?)</a>', text, flags=re.DOTALL)
    poems_ret= re.findall(r'<div class="contson".*?>(.*?)</div>', text, flags=re.DOTALL)
    poems=[]
    for poem in poems_ret:
        temp = re.sub("<.*?>", "", poem)
        poems.append(temp.strip())
    results = []
    for value in zip(titles, dynasty, authors, poems):
        title, time, author, poem = value
        result = {
            "标题": title,
            "朝代": time,
            "作者": author,
            "原文": poem
        }
 
        results.append(result)
    print(results)
def spider():
    #url_base = 'https://so.gushiwen.cn/shiwens/default.aspx?page={}&tstr=&astr=%E6%9D%8E%E7%99%BD'
    url_base = 'https://www.gushiwen.cn/default_{}.aspx'
    for i in range(1, 2):
        print('正在爬取第{}页：'.format(i))
        url = url_base.format(i)
        print(" " * 20 + "优美古诗文" + " " * 20)
 
        print("*" * 50)
        parse_page(url)
        print("*" * 50)
        return 
 
def data_save():
    poem_ls,poemist_ls,poemyw_ls = spider()
    del poem_ls[0]#删除一个多元元素
    length = len(poem_ls)
    if os.path.exists("E:/spyder_data/"):
        workbook = xlwt.Workbook(encoding="utf-8")
        worksheet = workbook.add_sheet("古诗词")
        worksheet.write(0, 0, "诗词名")
        worksheet.write(0, 1, "诗人名")
        worksheet.write(0, 2, "原文")
        for p in range(length):
            worksheet.write(p + 1, 0, poem_ls[p])
            worksheet.write(p + 1, 1, poemist_ls[p])
            worksheet.write(p + 1, 2, poemyw_ls[p])
            workbook.save('E:/spyder_data/poemyw.xls')
    else:
        os.mkdir('E:/spyder_data')
        workbook = xlwt.Workbook(encoding="utf-8")
        worksheet = workbook.add_sheet("古诗词")
        worksheet.write(0, 0, "诗词名")
        worksheet.write(0, 1, "诗人名")
        worksheet.write(0, 2, "原文")
        for p in range(length):
            worksheet.write(p + 1, 0, poem_ls[p])
            worksheet.write(p + 1, 1, poemist_ls[p])
            worksheet.write(p + 1, 2, poemyw_ls[p])
            workbook.save('E:/spyder_data/poemyw.xls')
 
 
 
 
if __name__ == '__main__':
    #spider()
    data_save()