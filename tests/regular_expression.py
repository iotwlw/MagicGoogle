# coding: utf-8

import re
str = "https://www.amazon.com/EnacFire-Reversible-PowerLine-Charging-Arranged/dp/B01F5AV0U8/ref=as_li_ss_tl?ie=UTF8&qid=1479697465&sr=8-1&keywords=reversible+usb+cable&linkCode=sl1&tag=learninginhan-20&linkId=b7de3c50f7d3e4d4be05de395e30c315"
print re.findall(r"dp/(\w{10})", str)[0]



num = 1

if num > 1:
    print num
# 发的萨芬

rating = '\xe7\x94\xa8\xe6\x88\xb7\xe8\xaf\x84\xe7\xba\xa7: 3/5\n2 \xe6\x9d\xa1\xe8\xaf\x84\xe8\xae\xba'
rating = rating.decode('utf-8')
# rating = rating.replace(u"用户评级: ", "")
review_num = re.search('\s(\d\.?\d?)/\d+\\n(\d+)', rating)
review_num = review_num.groups()
print review_num


review_value = re.search('bout\s(\d*,?\d*,?\d*,?\d*) results\s', 'Page 2 of about 4,420,000 results (0.62 seconds)')
review_value = review_value.group()
review_value = review_value.lstrip('bout ').rstrip(' results').replace(',', '')

print review_value
