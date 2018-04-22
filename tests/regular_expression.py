

import re
str = "https://www.amazon.com/EnacFire-Reversible-PowerLine-Charging-Arranged/dp/B01F5AV0U8/ref=as_li_ss_tl?ie=UTF8&qid=1479697465&sr=8-1&keywords=reversible+usb+cable&linkCode=sl1&tag=learninginhan-20&linkId=b7de3c50f7d3e4d4be05de395e30c315"
print re.findall(r"dp/(\w{10})", str)[0]



num = 1

if num > 1:
    print num

#http://www.jb51.net/article/99453.htm