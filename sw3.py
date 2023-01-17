
import requests
import codecs
import json
from bs4 import BeautifulSoup

DOWNLOAD_URL = 'https://so.gushiwen.org/authors/Default.aspx?p=1&c=%E5%94%90%E4%BB%A3'

def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(url, headers=headers).content
    return data
def parseHtml(html):
    soup = BeautifulSoup(html, features="html.parser")
    nextPage = 'https://so.gushiwen.org' + soup.find('a', attrs={'class': 'amore'}).get('href')
    leftDiv = soup.find('div', attrs={'class': 'main3'}).find('div', attrs={'class': 'left'})
    data = []
    for item in leftDiv.find_all('div', attrs={'class': 'sonspic'}):
        data.append('https://so.gushiwen.org' + item.find('a')['href'])
    return data, nextPage
def buildJson(keys, values):
    dictionary = dict(zip(keys, values))
    return json.dumps(dictionary)

def parseAuthorHtml(html):
    soup = BeautifulSoup(html, features="html.parser")
    all = soup.find('div', attrs={'class': 'main3'}).find('div', attrs={'class': 'left'})
    author = all.find('div', attrs={'class': 'sonspic'}).find('div', attrs={'class': 'cont'}).find('b').getText()
    desc = all.find('div', attrs={'class': 'sonspic'}).find('div', attrs={'class': 'cont'}).find('p').getText()
    sons = all.find('div',attrs={'class': 'sons'})
    yishiUrl = None
    if sons:
        yishiUrl = sons.get('id')
        if yishiUrl:
            yishiUrl = 'https://so.gushiwen.org/authors/ajaxziliao.aspx?id=' + all.find('div',attrs={'class': 'sons'})['id'].replace('fanyi','')
        else:
            yishiUrl = None
    return author, desc, yishiUrl

def parseAuthorMore(html):
    soup = BeautifulSoup(html, features='html.parser')
    yishi = []
    if soup.find('div', attrs={'clase', 'contyishang'}):
        for p in soup.find('div', attrs={'clase', 'contyishang'}).find_all('p'):
            yishi.append(p.getText())
    return ''.join(yishi)

def main():
    url = DOWNLOAD_URL
    keys = ['author', 'desc', 'story']
    with codecs.open('author.json', 'w', encoding='utf-8') as fp:
        fp.write('[')
        while url:
            html = download_page(url)
            data, url = parseHtml(html)
            for item in data:
                authorHtml = download_page(item)
                author, desc, yishiUrl = parseAuthorHtml(authorHtml)
                if yishiUrl:
                    yishiHtml = download_page(yishiUrl)
                    yishi = parseAuthorMore(yishiHtml)
                else:
                    yishi = ""
                fp.write(buildJson(keys, [author, desc,yishi]))
                fp.write(',')
        fp.write(']')

if __name__ == '__main__':
    main()
