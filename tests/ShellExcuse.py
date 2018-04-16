# coding: utf-8

import requests
import os
import time
#headers
headers = {
}

url='https://icanhazip.com/'


os.system('start G:\911S5\ProxyTool\AutoProxyTool.exe  -changeproxy/US')

time.sleep(5)

res = requests.get(url, headers=headers)
print res.content