#!/usr/bin/env python
# -*- coding: utf8 -*-

import copy

class SlotBasedCounter(object):
    '''
    provide per-slot counts of occurences of objects
    '''
    def __init__(self, numOfSlots):
        if numOfSlots <= 0:
            raise RuntimeError("Number of Slots must be greater than ZERO (you"
                    "requested " + str(numOfSlots) + ").")
            
        self.numOfSlots = numOfSlots
        self.objToCounts = {}


    def incrementCount(self, obj, slot, cnt = 1):
        if not self.objToCounts.has_key(obj):
            slots = [0] * self.numOfSlots 
            self.objToCounts[obj] = slots
        
        self.objToCounts[obj][slot] += cnt
            
    def getCount(self, obj, slot):
        if not self.objToCounts.has_key(obj):
            return 0
        else:
            return self.objToCounts[obj][slot]

    def getCounts(self):
        results = {}
        objToCounts = copy.deepcopy(self.objToCounts)   # deep copy
        for obj in objToCounts.iterkeys():
            totalCount = 0
            for count in objToCounts[obj]:
                totalCount += count
            results[obj] = totalCount
        return results

    def wipeSlot(self, slot):
        for k in self.objToCounts.iterkeys():
            self.objToCounts[k][slot] = 0

    def shouldBeRemoved(self, obj):
        totalCount = 0
        for count in self.objToCounts[obj]:
            totalCount += count

        return totalCount == 0


    def wipeZeros(self):
        '''travel the counter, and remove objects whose total count is ZERO'''
        toBeRemoved = []
        for k in self.objToCounts.iterkeys():
            if self.shouldBeRemoved(k):
                toBeRemoved.append(k)

        for k in toBeRemoved:
            del self.objToCounts[k]

if __name__ == '__main__':
    counter = SlotBasedCounter(5)
    for i in xrange(10):
        counter.incrementCount('M', 0)
        print counter.getCount('M', 0)

    counter.wipeSlot(0)
    print counter.getCounts()
    counter.wipeZeros()
    print counter.getCounts()
