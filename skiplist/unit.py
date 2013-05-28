#!/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from skip import SkipList

class SkipListTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_degenerated(self):
        '''
        When the maximun level is 1, the skiplist degenerated to a singly list
        '''
        l = SkipList(1)
        lines = open("./american-english-small").read().splitlines()
        for line in lines:
            if len(line) > 0:
                l.insert(line)

        self.assertEqual(l.find("A").elem, "A")
        self.assertEqual(l.find("B"), None)
        self.assertEqual(l.level, 1)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(SkipListTestCase("test_degenerated"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
