__author__ = 'Daemon1993'

import gevent
import requests
import time
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

SP = 1
Count=0

def getHtmlByFind(baseurl, page):
    url = baseurl + str(page)
    r = requests.session()

    html = r.get(url, timeout=5)

    #如果状态不正确 这里目的503 暂停时间增大一点
    if (html.status_code != 200):
        global SP
        SP += 0.5
        return

    #减少内存压力
    only_div_tag = SoupStrainer(id="content-left")

    # 先拿到这一块
    data = BeautifulSoup(html.text, "lxml",parse_only=only_div_tag)

    for tag in data.find_all("div", class_="article block untagged mb15"):
        name=tag.find("img").get('alt')
        content=tag.find("div",class_="content").text.strip()
        global Count
        Count+=1
        pass
        # print("\n 用户:{0} \n {1}".format(name,content))

    #每请求一次 睡眠一下
    time.sleep(SP)


def getHtmlBySelect(baseurl, page):
    url = baseurl + str(page)
    r = requests.session()

    html = r.get(url, timeout=5)

    if (html.status_code != 200):
        global SP
        SP += 0.5
        return

    #减小内存压力
    only_div_tag = SoupStrainer(id="content-left")

    # 先拿到这一块
    data = BeautifulSoup(html.text, "lxml",parse_only=only_div_tag)

    for tag in data.select('div[class="article block untagged mb15"]'):
        name=tag.select('img')[0].attrs.get('alt')
        content=tag.select('div[class="content"]')[0].get_text().strip()
        global Count
        Count+=1
        print("\n 用户:{0} \n\n {1}".format(name,content))

    #每请求一次 睡眠一下
    time.sleep(SP)


def useFind(baseurl):
    start=time.time()
    global  Count
    Count=0
    tasks = [gevent.spawn(getHtmlByFind, baseurl, index) for index in range(1, 50)]
    gevent.joinall(tasks)

    elapsed=time.time()-start
    print('getHtmlByFind time {0}  size{1}'.format(elapsed,Count))

def useSelect(baseurl):
    start=time.time()
    global  Count
    Count=0
    tasks = [gevent.spawn(getHtmlBySelect, baseurl, index) for index in range(1, 50)]
    gevent.joinall(tasks)

    elapsed=time.time()-start
    print('getHtmlBySelect time {0}  size{1}'.format(elapsed,Count))

if __name__ == '__main__':
    baseurl = "http://www.qiushibaike.com/8hr/page/"
    #useFind(baseurl)
    useSelect(baseurl)


