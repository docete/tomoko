#!/usr/bin/evn python
# -*- coding: utf8 -*-

import heapq
import random
import numpy as np
import sys

BIG_PRIME = 9223372036854775783

def random_parameter():
    return random.randrange(0, 9223372036854775783-1)

class CMSketch:
    """
    Count-Min sketch 是由 Graham Cormode 和 S. Muthu Muthukrishnan于2003年提出
    的一种概率数据结构，主要用来挖掘数据流中频繁项集。例如：Frequenes of 
    top-100 most frequent elements.该算法在容忍较低的错误率条件下能节省大量内存空间。
    https://en.wikipedia.org/wiki/Count-Min_sketch

    其原理是：
    1. 根据预先指定的错误率 \epsilon 和置信度 \delta, 初始化 w×d 的二维数组count，用于统计。
       其中，
               w = [e/epsilon]          # width of array
               d = [ln(1/delta)]        # depth of array
    2. 创建d个hash函数，其值域为 [0, w)
    3. 创建字典top_k，用于保存频繁项集，其中，键为 key, 值为 [estimate, key]
    4. 创建heap，用于更新top_k
    5. 插入元素：对集合S中的任意元素s，计算一组hash值
               H = {hi(s)} (i = 0...w-1)
       令 count[i, hi(s)] += 1, 同时更新top_k
    6. 更新top_k：
    7. 查询：对于任意元素s，
       取 estimate = min({ count[i][hi(s)] }) (i = 0...w-1), 即为元素s的估计值
    8. epsilon 与 delta

    缺陷：
    todo

    """
    def __init__(self, epsilon, delta, k):
        self.w = int(np.ceil(np.exp(1) / epsilon))
        self.d = int(np.ceil(np.log(1 / delta)))
        self.k = k

        self.hashfunctions = [self.__hash_function_generate() \
                for i in xrange(self.d)]
        self.count = np.zeros((self.d, self.w), dtype='int32')
        self.heap = []   # [(estimate, key)]
        self.top_k = {}  # {key: (estimate, key)}

    def update(self, key):
        for row, hashfunction in enumerate(self.hashfunctions):
            column = hashfunction(abs(hash(key)))
            self.count[row][column] += 1
        self.update_heap(key)

    def update_heap(self, key):
        estimate = self.get(key)
        if not self.heap or estimate >= self.heap[0][0]:
            if key in self.top_k:
                old_pair = self.top_k.get(key)
                old_pair[0] = estimate
                heapq.heapify(self.heap)
            else:
                if len(self.top_k) < self.k:
                    heapq.heappush(self.heap, [estimate, key])
                    self.top_k[key] = [estimate, key]
                else:
                    new_pair = [estimate, key]
                    old_pair = heapq.heappushpop(self.heap, new_pair)
                    if self.top_k.has_key(old_pair[1]):
                        del self.top_k[old_pair[1]]
                        self.top_k[key] = new_pair

    def get(self, key):
        value = sys.maxint
        for row, hashfunction in enumerate(self.hashfunctions):
            column = hashfunction(abs(hash(key)))
            estimate = self.count[row][column]
            value = min(value, estimate)
        return value

    def __hash_function_generate(self):
        a, b = random_parameter(), random_parameter()
        return lambda x: (a * x + b) % BIG_PRIME % self.w

if __name__ == '__main__':
    s = CMSketch(10**-7, 0.005, 100)
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        s.update(line[:-1])

    for k, v in sorted(s.top_k.iteritems(), key = lambda (k, v) : (v[0], k), reverse=True):
        print "%s\t%d" % (k, v[0])

