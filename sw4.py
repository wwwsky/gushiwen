'''
1,https://www.gushiwen.org/
2,用css选择器也能爬取网页信息，然后利用字符串函数讲字符串提取修整一下就可以，还是比较简单的！
这里，我设想，用css选择器和re正则表达式，都可以提取网页中我们想要的信息，只要熟练即可。
3，接下来，我提高一下难度，把爬取下来的故事，都写入到一个excel表格当中。

'''

import requests
from bs4 import BeautifulSoup
import time
from xlwt import *


poems = []  # 将故事变成了一个全局变量。


def parse_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    global poems
    response = requests.get(url, headers=headers)
    text = response.text
    soup = BeautifulSoup(text, 'lxml')  # 这里是分水岭，之前用正则，此时用beautifulsuop
    titles = soup.select(" div.cont > p > a > b")  # 返回的titles是一个列表
    #print(str(titles[0]).strip('<b>').rstrip('</b>'))  # 可以将旁边的<b>标签给去掉。成功得到了第一个标题。

    chaodais = soup.select("p.source > a:nth-child(1)")
    #print(chaodais[0].get_text()) # 这里成功提取出朝代。将链接等去掉。<a href="/shiwen/default.aspx?cstr=%e5%ae%8b%e4%bb%a3" target="_blank">宋代</a>
    authors = soup.select("p.source > a:nth-child(3)")
    #print(authors[0].get_text())
    # 返回的是一个列表。中间有好多网页标签，也需要处理。
    contents = soup.find_all("div", class_="contson")
    #print(contents[0].text)
    #创建一个列表，用来装数据
    for title, chaodai, author, content in zip(titles, chaodais, authors, contents):
        #创建一个字典，把每首古诗装入一个字典当中。
        data = {
            #"标题": title[0].strip('<b>').rstrip('</b>'),
            "标题": title.get_text(),
            "朝代": chaodai.get_text(),
            "作者": author.get_text(),
            "诗文": content.text.strip("\n")
        }
        poems.append(data)
    #print(poems)


def main():
    url = "https://www.gushiwen.org/default_1.aspx"

    for x in range(1, 8):
        url = "https://www.gushiwen.org/default_%s.aspx" % x
        parse_page(url)
        print(poems)  # 此时，得到的poems是一个全局变量！
        time.sleep(1)

    #接下来，我要将列表中的元素写入到excel表格当中，规规整整的！
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
        x = x + 1

    w.save('mini2.xls')


if __name__ == '__main__':
    main()
