# -*- coding:utf-8 -*-
from urllib import quote_plus

import requests
from lxml import etree
from MagicGoogle import MagicGoogle
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
PROXIES = [{
    'http': 'http://152.204.130.86:3128',
    'https': 'https://152.204.130.86:3128',
}]

# Or MagicGoogle()
mg = MagicGoogle(PROXIES)

postfix = open('./postfix', 'r')
postfixStr = postfix.readline()
def getfrombing():
  #  url='http://global.bing.com/search?q='+word+'&Accept-Language=en-us%3bq%3d0.5%2cen%3bq%3d0.3&Accept-Encoding=gzip%2c+deflate%2c+compress&Accept=text%2fhtml%2capplication%2fxhtml%2bxml%2capplication%2fxml%3bq%3d0.9%2c*%2f*%3bq%3d0.8&User-Agent=Mozilla%2f5.0+(X11%3b+Ubuntu%3b+Linux+x86_64%3b+rv%3a22.0)+Gecko%2f20100101+Firefox%2f22.0&Connection=keep-alive&Cache-Control=max-age%3d0&setmkt=en-us&setlang=en-us&FORM=SECNEN'

    word = "iphone cable" + postfixStr
    url = 'http://global.bing.com/search?q='+quote_plus(word)+'&qs=bs&ajf=60&first=1&Accept-Language=en-us'
    list = []
    # headers = {
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #     'Accept-Encoding': 'gzip, deflate, compress',
    #     'Accept-Language': 'en-us;q=0.5,en;q=0.3',
    #     'Cache-Control': 'max-age=0',
    #     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
    # }

    flag0 = 3
    #爬取网页的数量
    for k in range(0,100):
        headers = {'user-agent': mg.get_random_user_agent()}
        path = etree.HTML(requests.get(url=url, headers=headers).content.decode('utf-8'))
        flag=15
        if k == 0:
            flag=9

        flag0+=flag-1
        url='http://global.bing.com/search?q='+word+'&qs=bs&ajf=60&first='+str(flag0)+'&Accept-Language=en-us'
        print url
    return list


getfrombing()