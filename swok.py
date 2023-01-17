import re
import requests
from lxml import etree
import math
'''源地址'''
url_source = 'http://www.gushiwen.org/shiwen/'
'''模拟浏览器头部信息'''
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
'''获取所有的作者对应的作品的url'''
def get_auth_poey_urls():

    # response = urllib.request.urlopen(url).read().decode('utf-8')
    response = requests.get(url_source,headers=headers).text
    res = etree.HTML(response)
    urls = res.xpath('/html/body/div[2]/div[2]/div[2]/div[2]/a/@href')
    url_poey=[]
    for url in urls:
        url_poey.append('http://www.gushiwen.org'+str(url))
    return url_poey

'''获取每一个作者一共有多少篇文章，便于得到有多少页的信息'''
def get_poey_number(auth_poey_url):
    response = requests.get(auth_poey_url,headers).text
    number = re.findall('.*?<span style="color:#65645F; background-color:#E1E0C7; border:0px; width:auto;">共(.*?)篇',response)
    return int(number[0])

'''构造url得到所有作者所有页的url'''
def get_all_urls():
    all_urls = []
    flag = 1
    for url in get_auth_poey_urls():
        for i in range(1,math.ceil(get_poey_number(url)/10)+1):
            all_urls.append(url.replace(url[-6],str(i)))
            print('获取第'+str(flag)+'首诗词链接成功！')
            flag = flag+1
    return all_urls

'''获取内容'''
def get_content():
    try:
        fh = open('E:\spyder_data\poey.txt', 'a',encoding='utf-8')
        flag = 1
        for url in get_all_urls():
            response = requests.get(url, headers).text
            contents = re.findall(r'.*?id="txtare.*?>(.*?)http://so.gushiwen.org', response, re.S)
            print('爬取' + url + '的数据成功!')
            for content in contents:
                print('获取第'+str(flag)+'首诗词成功!-----'+str(re.findall(r'.*?《(.*?)》',content,re.S)[0]))
                flag = flag+1
                fh.write(content + '\n')
        fh.close()
    except Exception as e:
        print(e)

def main():
    get_content()

if __name__ == '__main__':
    main()


