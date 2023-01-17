import requests
import os
import re
import time
import xlwt

"""

#encoding="utf-8"
@Author:Mr.Pan_学狂
finish_time:2022/2/17 23:20
python爬取数据存储到Excel

"""


def spyder():
    url = "https://so.gushiwen.cn/gushi/tangshi.aspx"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3883.400 QQBrowser/10.8.4559.400"}
    response = requests.get(url,headers=headers)
    html = response.text
    # print(html)
    reg = '.aspx" target="_blank">(.*?)</a>'
    poem_name = re.findall(reg,html)
    # print(poem_name)
    reg2 = '</a>(.*?)</span>'
    poemist = re.findall(reg2,html)
    # print(poemist)
    poemist_ls = [poemor[1:-1] for poemor in poemist]
    # poemist_ls.remove(poemist_ls[0])
    # print(poemist_ls)
    return poem_name,poemist_ls

def data_save():
    poem_ls,poemist_ls = spyder()
    del poem_ls[0]#删除一个多元元素
    length = len(poem_ls)
    if os.path.exists("E:/spyder_data/"):
        workbook = xlwt.Workbook(encoding="utf-8")
        worksheet = workbook.add_sheet("古诗词")
        worksheet.write(0, 0, "诗词名")
        worksheet.write(0, 1, "诗人名")
        for p in range(length):
            worksheet.write(p + 1, 0, poem_ls[p])
            worksheet.write(p + 1, 1, poemist_ls[p])
            workbook.save('E:/spyder_data/poem.xls')
    else:
        os.mkdir('E:/spyder_data')
        workbook = xlwt.Workbook(encoding="utf-8")
        worksheet = workbook.add_sheet("古诗词")
        worksheet.write(0, 0, "诗词名")
        worksheet.write(0, 1, "诗人名")
        for p in range(length):
            worksheet.write(p + 1, 0, poem_ls[p])
            worksheet.write(p + 1, 1, poemist_ls[p])
            workbook.save('E:/spyder_data/poem.xls')
    # if len(poem_ls) == len(poemist_ls):
    #     print(True)
    # else:
    #     print(False)

if __name__ == '__main__':
    # spyder()
    data_save()
