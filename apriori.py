# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 15:49:29 2015

@author: Administrator
"""
import itertools
import copy
from dataSource import *

# 初始化候选1项集
def c1Create(data):
    c1 = set(data[0])
    for da in data:
        c1.update(set(da))
    return list(c1)

# 支持度计数
def frequenceCreate(candidate, data, k):
    result = []    
    support_count = []
    #support_print = []  # for print
    for i, cd in enumerate(candidate):
        support_count.append(0)
        for da in data:
            if set(cd).issubset(set(da)):
                support_count[i] += 1
    for i, sp in enumerate(support_count):
        if sp >= k:
            result.append(candidate[i])            
            #support_print.append(sp)  #for print
    #return zip(result, support_print)
    return result
    
# 利用先验定理对candidate进行剪枝    
def preTest(candidate, frequence):
    result = copy.deepcopy(candidate)
    print 'result', result #
    num = len(frequence[0]) + 1
    for cd in candidate:
       # print 'cd', cd #
        for i in itertools.combinations(cd, num-1):
           # print 'i', i #
            temp = list(i)
            tag = 0
            for fr in frequence:
               # print 'fr', fr #
                print temp[0], fr
                if temp[0] == fr:
                    tag == 1
                    break
            if tag == 0:
                result.remove(cd)
                break
    return result

# 从frequence(频繁num-1项集)创建candidate(候选num项集)    
def candidateCreate(frequence):
    result = []
    num = len(frequence[0]) + 1
    for i in range(len(frequence)):
        for j in range(i, len(frequence)):
            temp = set(frequence[i])
            temp.update(set(frequence[j]))
            if (len(temp) == num) & (list(temp) not in result):
                result.append(list(temp))
    result = preTest(result, frequence)
    return result
    
