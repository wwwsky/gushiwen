
# author:Simple-Sir
# time:2019/7/31 22:01
# 爬取古诗文网页数据
import re
import requests
from bs4 import BeautifulSoup
import time
from xlwt import *

poems = []  # 将故事变成了一个全局变量。

def getHtml(page):
    '''
    获取网页数据
    :param page:  页数
    :return:  网页html数据(文本格式)
    '''
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    url = 'https://www.gushiwen.org/default_{}.aspx'.format(page)  # 获取几页数据
    respons = requests.get(url, headers=headers)
    html = respons.text
    return html


def getText(html):
    # 获取标题 re.DOTALL 匹配所有字符，包含\n（.无法匹配\n）
    titles = re.findall(r'<div class="cont">.*?<b>(.*?)</b>', html, re.DOTALL)
    caodai = re.findall(
        r'<p class="source">.*?<a.*?>(.*?)</a>', html, re.DOTALL)  # 获取朝代
    author = re.findall(
        r'<p class="source">.*?<a.*?>.*?<a.*?>(.*?)</a>', html, re.DOTALL)  # 获取朝代
    contents = re.findall(
        r'<div class="contson".*?>(.*?)</div>', html, re.DOTALL)  # 获取诗文，包含标签符号
    con_texts = []  # 诗文，不含标签符号
    for i in contents:
        rsub = re.sub('<.*?>', '', i)
        con_texts.append(rsub.strip())  # strip 去空格
    
    global poems

    for v in zip(titles, caodai, author, con_texts):
        bt, cd, zz, sw = v
        data = {
            '标题': bt,
            '朝代': cd,
            '作者': zz,
            '诗文': sw
        }
        poems.append(data)
    return poems


def main():
    p = int(input('您想要获取多少页的数据？\n'))
    for page in range(1, p+1):
        print('第{}页数据：'.format(page))
        html = getHtml(page)
        text = getText(html)
        #for i in text:
          #  print(i)

    w = Workbook()  # w必须是大写，此步骤创建了一个工作簿。
    ws = w.add_sheet('这是古诗')  # 此步骤创建了一个名字是 xlwt was here的工作表。
    ws.write(0, 0, "标题")
    ws.write(0, 1, "朝代")
    ws.write(0, 2, "作者")
    ws.write(0, 3, "诗文")

    x = 1
    for data in poems:
        print(data)
        ws.write(x, 0, data["标题"])  # 在第2行1列的单元格（cell）中,输入foot。注意,首行首列都是从0开始的。
        ws.write(x, 1, data["朝代"])
        ws.write(x, 2, data["作者"])
        ws.write(x, 3, data["诗文"])
        w.save('gushiwen1.xls')
        x = x + 1
        

    w.save('gushiwen.xls')




if __name__ == '__main__':
    main()
