from MagicBing import MagicBing
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

PROXIES = [{
    'http': 'http://152.204.130.86:3128',
    'https': 'https://152.204.130.86:3128',
}]

mg = MagicBing(PROXIES)

postfix = open('../config/postfix', 'r')
postfixStr = postfix.readline()

result_list = []
csv_prefix_name = "ALL"
headers = ['title', 'rating', 'star', 'review', 'url']

keywords = open('./keywords', 'r')
for keyword in keywords:
    keyword = keyword.strip()

    result_keyword = []

    for p in range(0, 80):
        first = p * 10 + 1
        result_keyword_one = mg.search(query=keyword + postfixStr, start=first, keyword=keyword)
        result_keyword = result_keyword + result_keyword_one

    mg.dict_list_to_csv_file(result_list=result_keyword, csv_prefix_name=keyword, headers=headers)
