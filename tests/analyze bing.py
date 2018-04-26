# coding=UTF-8
# This Python file uses the following encoding: utf-8
import os
import sys
import pprint

import re

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from MagicBing import MagicBing

mg = MagicBing()
postfix = open('./postfix', 'r')
postfixStr = postfix.readline()

# mg.search(query="iphone cable" + postfixStr, first=1, keyword="iphone cable")

google2amazon_results = open('./log/Connectors Adapters-11 2018-04-25 15;33;10.html', 'r')
google2amazon_result = google2amazon_results.read()

pq_content = mg.pq_html(google2amazon_result)
for item in pq_content('li.b_algo').items():
    title = item('div.b_title>h2>a').eq(0).text()
    href = item('div.b_title>h2>a').eq(0).attr('href')
    rating = ""
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


# s = rating.encode('utf-8')
# print s.strip('')
# print s.lstrip('Rating: ')
# print s.rstrip(' reviews')
# print s.lstrip('Rating: ').rstrip(' reviews')
# a = s.replace("\xc2\xa0", "").lstrip('Rating: ').rstrip(' reviews')
# b = a.split('-')
# print(a.split('-'))
