#!/usr/bin/env python
# -*- coding: utf8 -*-

from SlotBasedCounter import SlotBasedCounter

class SlidingWindowCounter(object):
    '''
    
    '''
    def __init__(self, windowLengthInSlots):
        if windowLengthInSlots < 2:
            raise RuntimeError("window length in slots must be at least TWO (" \
                    "you requested " + str(windowLengthInSlots) + ")")

        self.windowLengthInSlots = windowLengthInSlots
        self.objCounter = SlotBasedCounter(windowLengthInSlots)
        self.headSlot = 0
        self.tailSlot = self.slotAfter(self.headSlot)

    def incrementCount(self, obj, cnt = 1):
        self.objCounter.incrementCount(obj, self.headSlot, cnt)

    def getCountsThenAdvanceWindow(self):
        counts = self.objCounter.getCounts()
        self.objCounter.wipeZeros()
        self.objCounter.wipeSlot(self.tailSlot)
        self.advanceWindow()
        return counts

    def advanceWindow(self):
        self.headSlot = self.tailSlot
        self.tailSlot = self.slotAfter(self.headSlot)

    def slotAfter(self, slot):
        return (slot + 1) % self.windowLengthInSlots

if __name__ == '__main__':
    from random import randint
    counter = SlidingWindowCounter(5)

    words = ["dahon", "trek", "gaint", "mereda"]
    for i in xrange(1000):
        idx = randint(0, 3)
        
        if i % 10  == 0:
            print counter.getCountsThenAdvanceWindow()
        
        counter.incrementCount(words[idx])

