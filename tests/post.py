#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4:et

import sys
import pycurl


class Test:
    def __init__(self):
        self.contents = ''

    def body_callback(self, buf):
        self.contents = self.contents + buf
        f = open('f:\\tmp\\tmp.html', 'w')
        print f
        f.write(self.contents)


sys.stderr.write("Testing %s\n" % pycurl.version)

t = Test()
c = pycurl.Curl()
c.setopt(c.URL, 'https://www.google.com/search?q=testx')

c.setopt(c.USERAGENT, "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0) in my heart of heart.")
c.setopt(c.HEADER, True)
c.setopt(c.REFERER, "https://www.google.com/search?q=testx")
c.setopt(c.COOKIEFILE, "./COOKIE.txt")
c.setopt(c.COOKIEJAR, "./COOKIE.txt")

c.setopt(c.WRITEFUNCTION, t.body_callback)
c.perform()
c.close()

print(t.contents)



