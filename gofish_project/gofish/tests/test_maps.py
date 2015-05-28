from unittest import TestCase
from gofish.engine.maps import *

"""
The contract of these functions is such that they don't handle
error conditions, they assume all inputs are valid
"""

class MapGeneratorTest(TestCase):
    def test_generate(self):
        depths = [1, 5, 10, 15, 50]
        widths = [1, 5, 10, 15, 50]
        # the generation is random, so we will generate
        # map with many times and see if it is always
        # within the specified bounds, increasing our confidence
        for depth in depths:
            for width in widths:
                for i in range(0, 100):
                    lake = generate(depth, width)
                    self.assertEqual(len(lake[0]), width)
                    for j in range(0, width):
                        self.assertTrue(lake[0][j] > 0)
                        self.assertTrue(lake[0][j] <= depth)
