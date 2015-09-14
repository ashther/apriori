# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 15:51:54 2015

@author: Administrator
"""

data = []

f = open('data.txt', 'r')
for line in f.readlines():
    data.append(line.strip('\r\n').split(','))
f.close()