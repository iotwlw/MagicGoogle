# -*- coding:utf-8 -*-
from urllib import quote_plus

import cchardet
import requests
from MagicGoogle import MagicGoogle
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
PROXIES = [{
    'http': 'http://152.204.130.86:3128',
    'https': 'https://152.204.130.86:3128',
}]

mg = MagicGoogle(PROXIES)

postfix = open('./postfix', 'r')
postfixStr = postfix.readline()


def getfrombing():
    keywords = open('./keywords', 'r')
    for keyword in keywords:
        keyword = keyword.rstrip()

        word = keyword + postfixStr
        url = 'http://global.bing.com/search?q='+quote_plus(word)+'&qs=bs&ajf=60&first=1&Accept-Language=en-us'

        flag0 = 3

        for k in range(0, 100):
            try:
                headers = {'user-agent': mg.get_random_user_agent()}
                r = requests.get(url=url, headers=headers)
                content = r.content
                charset = cchardet.detect(content)
                text = content.decode(charset['encoding'])
                flag=14
                if k == 0:
                    flag=9
                flag0+=flag-1
                mg.content_to_html(content_html=text, log_prefix_name=keyword + '-' + str(flag0) + ' ')
                url='http://global.bing.com/search?q='+word+'&qs=bs&ajf=60&first='+str(flag0)+'&Accept-Language=en-us'
                print url
            except Exception as e:
                print("------------------------------------------------------------{}".format(e))

getfrombing()
