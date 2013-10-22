#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import random
import math
import heapq

class ReservoirSampling(object):
    '''
    Sampling from a stream of elements
    '''
    def __init__(self, numOfSamples, container=[]):
        self.numOfSamples = numOfSamples
        self.container = container
        self.samples = []

    def sample(self):
        for i, item in enumerate(self.container):
            if i < self.numOfSamples:
                self.samples.append(item)
            elif i >= self.numOfSamples \
                    and random.random() < self.numOfSamples / float(i+1):
                replace = random.randint(0, len(self.samples)-1)
                self.samples[replace] = item

    def dump(self):
        print self.samples

class WeightedReservoirSampling(object):
    def __init__(self, numOfSamples, container=[]):
        self.numOfSamples = numOfSamples
        self.container = container
        self.samples = []

    def sample(self):
        heaped = False
        for i, item in enumerate(self.container):
            w = item['weight']
            r = random.random()
            k = math.pow(r, 1.0/w)

            if i < self.numOfSamples:
                self.samples.append((k, item))
            elif i >= self.numOfSamples:
                if not heaped:
                    heapq.heapify(self.samples)
                    headed = True
                heapq.heappushpop(self.samples, (k, item))
            
    def dump(self):
        print self.samples

if __name__ == '__main__':
    fd = open('/usr/share/dict/american-english', 'r')
    #lines = []
    #for line in fd:
    #    line = line[:-1]

    #    if len(line) == 0:
    #        continue

    #    item = {}
    #    item['data'] = line
    #    lines.append(item)
    #fd.close()

    rs = ReservoirSampling(10, fd)
    rs.sample()
    rs.dump()
    fd.close()

    fd = open('/usr/share/dict/american-english', 'r')
    weighted_lines = []
    for line in fd:
        line = line[:-1]
        if len(line) == 0:
            continue

        item = {}
        item['weight'] = len(line)
        item['data'] = line
        weighted_lines.append(item)
    fd.close()

    wrs = WeightedReservoirSampling(10, weighted_lines)
    wrs.sample()
    wrs.dump()

