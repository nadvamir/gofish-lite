from unittest import TestCase
from gofish.engine.yields import *

"""
The contract of these functions is such that they don't handle
error conditions, they assume all inputs are valid
"""

class YieldsHelpersTest(TestCase):
    def test_positive(self):
        self.assertEqual(positive(5), 5)
        self.assertEqual(positive(0), 0)
        self.assertEqual(positive(-5), 0)

    def test_nth(self):
        self.assertEqual(nth(0, 3, 1.0, 0.2), 0)
        self.assertEqual(nth(1, 3, 1.0, 0.2), 0)
        self.assertEqual(nth(2, 3, 1.0, 0.2), 1.0)
        self.assertEqual(nth(3, 3, 1.0, 0.2), 0)
        self.assertEqual(nth(4, 3, 1.0, 0.2), 0)
        self.assertEqual(nth(5, 3, 1.0, 0.2), 0.8)
        self.assertEqual(nth(6, 3, 1.0, 0.2), 0)

class YieldsTest(TestCase):
    def test_makeUniformDecliningYield(self):
        options = {'zero-at': 4}
        y = makeUniformDecliningYield(5, options)
        self.assertEqual(y, [1, 0.75, 0.5, 0.25, 0.0])

        options = {'zero-at': 2}
        y = makeUniformDecliningYield(4, options)
        self.assertEqual(y, [1, 0.5, 0, 0])

        options = {'zero-at': 10}
        y = makeUniformDecliningYield(4, options)
        self.assertEqual(y, [1, 0.9, 0.8, 0.7])

    def test_makeUniformConstantYield(self):
        options = {'val': 0.5}
        y = makeUniformConstantYield(4, options)
        self.assertEqual(y, [0.5, 0.5, 0.5, 0.5])

    def test_makeUniformRandomYield(self):
        options = {'lower': 0.3, 'upper': 0.7}
        y = makeUniformRandomYield(1000, options)
        self.assertEqual(len(y), 1000)
        for val in y:
            self.assertTrue(val >= 0.3)
            self.assertTrue(val <= 0.7)

    def test_makeNthDecliningYield(self):
        options = {'n': 3, 'zero-at-n': 10}
        y = makeNthDecliningYield(12, options)
        target = [0, 0, 1.0, 0, 0, 0.9, 0, 0, 0.8, 0, 0, 0.7]
        self.assertEqual(y, target)

    def test_makeNthConstantYield(self):
        options = {'n': 3, 'val': 0.5}
        y = makeNthConstantYield(12, options)
        target = [0, 0, 0.5, 0, 0, 0.5, 0, 0, 0.5, 0, 0, 0.5]
        self.assertEqual(y, target)

