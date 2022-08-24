import urllib.request as req
from lxml import etree
import os
prefix = r'http://www.kekenet.com/broadcast/Normal/Jan21VOAxia/'
max_page = 9
items = []
save_path = './results/'

def openUrl(url):
    return req.urlopen(req.Request(url)).read()

input()


urls = []
for i in range(1,max_page+1):
    if(i == max_page):
        url = prefix
    else:
        url = prefix + f'List_{i}.shtml'
    root = etree.HTML(openUrl(url))
    tmp = [r'http://www.kekenet.com'+j for j in root.xpath(r"//*[@id='menu-list']/li/a[@href!='#']/@href")]
    tmp.reverse()
    urls.extend(tmp)

cnt = 0
for url in urls:
    idx = int(url.split('/')[-1].split('.')[0])
    if(idx < 644761):
        continue
    cnt += 1
    root = etree.HTML(openUrl(url))
    title = root.xpath(r"//h1[@id='nrtitle']/text()")[0]
    print(title)

    name = format(cnt, '0>2d') + '-' + title
    if(not os.path.exists(save_path + name)):
        os.mkdir(save_path + name)

    texts = root.xpath(r"//div[@class='qh_en']/p/text()|//div[@class='qh_zg']/p/text()")
    with open(save_path + name + '/' + title +'.txt', 'w', encoding = 'utf-8') as f:
        for text in texts:
            f.write(text + '\n')

    audio = openUrl(root.xpath(r"//audio/@src")[0])
    with open(save_path + name + '/' + title +'.mp3', 'wb') as f:
        f.write(audio)
    

