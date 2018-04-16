# coding: utf-8

import requests
proxies = {
    'http': 'http://127.0.0.1:48850',
    'https': 'https://127.0.0.1:48850',
}
headers = {'user-agent': 'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.5.22 Version/10.50'}

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
r = requests.get(url='https://www.google.com/',
                 # proxies=proxies,
                 headers=headers,
                 allow_redirects=False,
                 verify=False,
                 timeout=30)
content = r.content
print content
