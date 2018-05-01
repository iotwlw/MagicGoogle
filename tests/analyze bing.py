# coding=UTF-8
# This Python file uses the following encoding: utf-8
import os
import sys
import pprint

import re

import cchardet
import requests

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from MagicBing import MagicBing

mg = MagicBing()
url = "https://cn.bing.com/search?q=Headphone++Accessories%22we+don%27t+know+when+or+if+this+item+will+be+back+in+stock%22+site%3awww.amazon.com&qs=bs&first=51"
proxies = {
    'http': 'http://39.134.68.4:80',
    'https': 'https://39.134.68.4:80',
}
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en_US,en;q=0.8'
    }

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
r = requests.get(url=url,
                 # proxies=proxies,
                 headers=headers)
print ("URL_INFO:{}".format(url))
content = r.content
print content

charset = cchardet.detect(content)
text = content.decode(charset['encoding'])

pq_content = mg.pq_html(text)
for item in pq_content('li.b_algo').items():
    title = item('h2>a').eq(0).text()
    href = item('h2>a').eq(0).attr('href')
    rating = ""
    star = ""
    review = ""
    if item('div.b_vlist2col'):
        rating = item('div.b_vlist2col').eq(0).text()
        rating_out = re.search('\s(\d\.?\d?)/\d+\\n(\d+)', rating)
        rating_out = rating_out.groups()
        star = rating_out[0]
        review = rating_out[1]

    result_dict = {"title": title,
                   "href": href,
                   "rating": rating,
                   "star": star,
                   "review": review,
                   }

    pprint.pprint(result_dict)


