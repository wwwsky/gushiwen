import time

import requests
from lxml import etree
from multiprocessing import Pool


#先创建一个lp文件夹


def zxc(qwe, hercx):
  qwe_op = requests.get(qwe, headers=hercx).text
  html1 = etree.HTML(qwe_op)
  '标头的xpth的'
  roto = html1.xpath('//*[@id="sonsyuanwen"]/div[1]/h1/text()')
  "作者的xpth"
  roto1 = html1.xpath('//*[@id="sonsyuanwen"]/div[1]/p/a[1]/text()')
  '诗句'
  textuio = html1.xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[2]/text()')
  with open('lp/'+str(roto[0])+'.txt', 'a+', encoding='utf-8')as ll:
     ll.write('{}\n'.format(str(roto[0])))
     ll.write('{}\n'.format(str(roto1[0])))
     for i in textuio:
       s = str(i).replace(' ', '')
       ll.write('{}\n'.format(str(s)))
  print('完成{}下载'.format(roto[0]))


# 用进程池
if __name__ == '__main__':
   qwe1 = time.time()
   pool = Pool()
   hercx = {
       'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.25'
   }
   cvb = requests.get(
       'https://so.gushiwen.cn/gushi/tangshi.aspx/', headers=hercx).text
   html = etree.HTML(cvb)

   '爬取300首古诗 获取300首的地址xpath'
   qwe_300 = '//*[@id="html"]/body/div/div/div/div/span/a/@href'
   rahsfd_300 = html.xpath(qwe_300)
   vbn_to = rahsfd_300  # 300个地址返回成列表里面

   adp = 'https://so.gushiwen.cn'
   for i in vbn_to:
       qwe = adp+str(i)
       pool.apply_async(zxc, args=(qwe, hercx))
   cvb = time.time()
   pool.close()
   pool.join()
   print('{}秒'.format(str(cvb-qwe1)))
