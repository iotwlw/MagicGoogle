#!/usr/bin/env python
# coding=utf-8
# code by 92ez.com

import subprocess
import time
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')


def change_ip_for_vps():
    try:
        subprocess.Popen('pppoe-stop', shell=True, stdout=subprocess.PIPE)
        time.sleep(5)
        subprocess.Popen('pppoe-start', shell=True, stdout=subprocess.PIPE)
        time.sleep(5)
        pppoe_restart = subprocess.Popen('pppoe-status', shell=True, stdout=subprocess.PIPE)
        pppoe_restart.wait()
        pppoe_log = pppoe_restart.communicate()[0]
        adsl_ip = re.findall(r'inet (.+?) peer ', pppoe_log)[0]
        print '[*] New ip address : ' + adsl_ip
        return True
    except Exception, e:
        print e
        change_ip_for_vps()

if __name__ == '__main__':
    count = 1
    while True:
        print '[*] NEXT %s ADSL' % str(count)
        change_ip_for_vps()
        count += 1