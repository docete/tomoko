#!/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from SlotBasedCounter import SlotBasedCounter
from SlidingWindowCounter import SlidingWindowCounter

def newInstanceSlotBasedCounter(numberOfSlots):
    counter = SlotBasedCounter(numberOfSlots)

class SlotBasedCounterTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def newInstanceShouldHaveEmptyCounts(self):
        counter = SlotBasedCounter(1)
        self.assertEqual(0, len(counter.getCounts()))

    def numberOfSlotsShouldGreaterThanZero(self):
        self.assertRaises(RuntimeError, newInstanceSlotBasedCounter, 0)
        self.assertRaises(RuntimeError, newInstanceSlotBasedCounter, -1)

    def shouldReturnNonEmptyCountsWhenAtLeastOneObjectWasCounted(self):
        ANY_OBJECT = "ANY_OBJECT"
        ANY_SLOT = 0
        ANY_NUM_SLOTS = 1

        counter = SlotBasedCounter(ANY_NUM_SLOTS)
        counter.incrementCount(ANY_OBJECT, ANY_SLOT)

        self.assertEqual(1, len(counter.getCounts()))
        self.assertEqual(1, counter.getCount(ANY_OBJECT, ANY_SLOT))

    def wipeSlotShouldSetAllCountsInSlotsToZero(self):
        ANY_NUM_SLOTS = 1
        ANY_SLOT = 0
        countWasOne = "countWasOne"
        countWasThree = "countWasThree"

        counter = SlotBasedCounter(ANY_NUM_SLOTS)

        counter.incrementCount(countWasOne, ANY_SLOT)
        counter.incrementCount(countWasThree, ANY_SLOT)
        counter.incrementCount(countWasThree, ANY_SLOT)
        counter.incrementCount(countWasThree, ANY_SLOT)

        self.assertEqual(1, counter.getCount(countWasOne, ANY_SLOT))
        self.assertEqual(3, counter.getCount(countWasThree, ANY_SLOT))

        counter.wipeSlot(ANY_SLOT)


        self.assertEqual(0, counter.getCount(countWasOne, ANY_SLOT))
        self.assertEqual(0, counter.getCount(countWasThree, ANY_SLOT))

    def wipeZerosShouldRemoveAnyObjectsWithZeroTotalCount(self):
        counter = SlotBasedCounter(2)
        wipeSlot = 0
        otherSlot = 1

        willBeRemored = "willBeRemored"
        willContinueToBeTrack = "willContinueToBeTrack"

        counter.incrementCount(willBeRemored, wipeSlot)
        counter.incrementCount(willContinueToBeTrack, wipeSlot)
        counter.incrementCount(willContinueToBeTrack, otherSlot)

        counter.wipeSlot(wipeSlot)
        counter.wipeZeros()

        self.assertFalse(counter.getCounts().has_key(willBeRemored), "%s has been removed by wipeZeros" % willBeRemored)
        self.assertTrue(counter.getCounts().has_key(willContinueToBeTrack), "%s will continue to be tracked" % willContinueToBeTrack)

class SlidingWindowCounterTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(SlotBasedCounterTestCase("newInstanceShouldHaveEmptyCounts"))
    suite.addTest(SlotBasedCounterTestCase("numberOfSlotsShouldGreaterThanZero"))
    suite.addTest(SlotBasedCounterTestCase("shouldReturnNonEmptyCountsWhenAtLeastOneObjectWasCounted"))
    suite.addTest(SlotBasedCounterTestCase("wipeSlotShouldSetAllCountsInSlotsToZero"))
    suite.addTest(SlotBasedCounterTestCase("wipeZerosShouldRemoveAnyObjectsWithZeroTotalCount"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
