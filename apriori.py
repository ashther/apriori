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

# 从candidate(候选num项集)创建frequence(频繁num项集)  
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
    num = len(frequence[0]) + 1
    for cd in candidate:
        for i in itertools.combinations(cd, num-1):
            tag = 0
            for fr in frequence:
                if set(i) == set(fr):
                    tag = 1
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

# 从data创建支持度阈值为k的频繁项集集合 
def frequenceItemCreate(data, k):
    frequence_item = []
    c1 = c1Create(data)
    num = 1
    while True:
        candidate = c1 if num == 1 else candidate
        frequence = frequenceCreate(candidate, data, k)
        if len(frequence) == 0:
            break
        frequence_item.append(frequence)
        candidate = candidateCreate(frequence)
        num += 1 
    return frequence_item

# 从items(一维list)创建其所有非空子集，输出为长度n的list，每个元素又是长度为2的list，
# 每个元素是一维list
def subsetCreate(items):
    result = []
    for num in range(1, len(items)):
        for combn in itertools.combinations(items, num):
            temp = copy.deepcopy(items)
            for c in combn:
                temp.remove(c)
            result.append([list(combn), temp])
    return result

# 从frequence_item创建关联规则，置信度阈值为confidence, 事物集为data
# frequence_item有n个元素，每个元素是list，其中list内的元素也是list(除第一项)
def rulesCreate(frequence_item, data, confidence):
    result = []
    conf = []
    rules = {}
    for items in frequence_item:
        if len(items[0]) == 1:
            for subset in subsetCreate(items):
                result.append(subset)
                conf.append(0)
                tmp1, tmp2 = 0, 0
                for da in data:
                    if set(subset[0]).issubset(set(da)):
                        tmp2 += 1
                        if set(subset[1]).issubset(set(da)):
                            tmp1 += 1
                try:
                    conf[-1] = float(tmp1) / float(tmp2)
                except ZeroDivisionError:
                    conf[-1] = 0
        else:
            for item in items:
                for subset in subsetCreate(item):
                    result.append(subset)
                    conf.append(0)
                    tmp1, tmp2 = 0, 0
                    for da in data:
                        if set(subset[0]).issubset(set(da)):
                            tmp2 += 1
                            if set(subset[1]).issubset(set(da)):
                                tmp1 += 1
                    try:
                        conf[-1] = float(tmp1) / float(tmp2)
                    except ZeroDivisionError:
                        conf[-1] = 0
                              
    for i, res in enumerate(result):
        if conf[i] >= confidence:
            rules[str(res)] = conf[i]
    return rules
    
if __name__ == '__main__':
    k = 2
    confidence = 0.1
    frequence_item = frequenceItemCreate(data, k)
    rules = rulesCreate(frequence_item, data, confidence)
    # 排序后rules由dict变为list
    rules = sorted(rules.iteritems(), key=lambda x:x[1], reverse=True)
    for r in rules:
        print '%s : %.2f' %(r[0], r[1])
    




























