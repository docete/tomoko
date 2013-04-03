#!/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from BloomFilter import BloomFilter

class BloomFilterTestCase(unittest.TestCase):
    def setUp(self):
        self.bf = BloomFilter(262144, 14)
        lines = open("/usr/share/dict/american-english").read().splitlines()
        for line in lines:
            self.bf.update(line)

    def tearDown(self):
        pass

    def test_probably(self):
        self.assertEqual(self.bf.lookup("Max"), "Probably")
        self.assertEqual(self.bf.lookup("mice"), "Probably")

    def test_nope(self):
        self.assertEqual(self.bf.lookup("3"), "Nope")
        self.assertEqual(self.bf.lookup("google"), "Nope")



if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(BloomFilterTestCase("test_probably"));
    suite.addTest(BloomFilterTestCase("test_nope"));
    runner = unittest.TextTestRunner()
    runner.run(suite)
