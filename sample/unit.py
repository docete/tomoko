#!/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from sampling import ReservoirSampling, WeightedReservoirSampling

class WeightedReservoirSamplingTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testEqualprobably(self):
        items = [\
                {"weight": 1, "data": "Alen"},\
                {"weight": 1, "data": "John"},\
                ]

        countOfAlen = 0
        countOfJohn = 0

        counts = 100000
        for i in xrange(counts):
            wrs = WeightedReservoirSampling(1, items)
            wrs.sample()

            if len(wrs.samples) == 1 \
                    and wrs.samples[0][1]["data"] == "Alen":
                countOfAlen += 1

            if len(wrs.samples) == 1 \
                    and wrs.samples[0][1]["data"] == "John":
                countOfJohn += 1

        self.assertTrue(
                abs(countOfAlen-countOfJohn) * 1.0 / counts < 0.01,
                "Diff of Count should smaller than 1%% : Alen [%d] and John [%d]" % (countOfAlen, countOfJohn))

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(WeightedReservoirSamplingTestCase("testEqualprobably"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
