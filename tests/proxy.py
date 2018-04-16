# coding: utf-8

import requests
#proxy
# SOCKS5 proxy for HTTP/HTTPS
proxies = {
    'http': 'http://192.168.1.103:48850',
    'https': 'https://192.168.1.103:48850',
}

#headers
headers = {
}

url='https://icanhazip.com/'
res = requests.get(url, headers=headers
                   # , proxies=proxies
                   )
print res.content