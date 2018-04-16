#!/usr/bin/python
# -*- coding: UTF-8 -*-
var = 3  # 第二个实例
while var > 0:
    for letter in 'Python':  # 第一个实例
        if letter == 'h':
            break
        print '当前字母 :', letter
    var = var - 1

print "Good bye!"