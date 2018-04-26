# coding=UTF-8
# This Python file uses the following encoding: utf-8
import os
import sys
import pprint

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from MagicGoogle import MagicGoogle

################################################
# """
# cd MagicGoogle
# python Examples/search_result.py
# """
#################################################

PROXIES = [{
    'http': 'http://127.0.0.1:1080',
    'https': 'http://127.0.0.1:1080'
}]

# Or MagicGoogle()
mg = MagicGoogle(PROXIES)

google2amazon_results = open('./Connectors Adapters-11 2018-04-25 00;21;03.html', 'r')
google2amazon_result = google2amazon_results.read()

pq_content = mg.pq_html(google2amazon_result)
for item in pq_content('div.g').items():
    result = {'title': item('h3.r>a').eq(0).text()}
    href = item('h3.r>a').eq(0).attr('href')
    rating = item('div.f.slp').eq(0).text()
    if href:
        url = mg.filter_link(href)
        result['url'] = url
    text = item('span.st').text()
    result['text'] = text
    pprint.pprint(result)


s = rating.encode('utf-8')
print s.strip('')
print s.lstrip('Rating: ')
print s.rstrip(' reviews')
print s.lstrip('Rating: ').rstrip(' reviews')
a = s.replace("\xc2\xa0", "").lstrip('Rating: ').rstrip(' reviews')
b = a.split('-')
print(a.split('-'))

print b[0]