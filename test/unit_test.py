import sys
import unittest
from utils import math_utils
import math


class UnitTest(unittest.TestCase):
    @unittest.skip
    def test_something(self):
        shape1 = [(0, 0), (1, 0), (0, 1)]
        shape2 = [(2, 0), (3, 1), (1, 1)]
        vector = (1, 0)
        p = math_utils.support(shape1, shape2, vector)
        expected = 0, -1
        self.assertEqual(expected, p)
        shape3 = [(-1, -1), (1, 0), (0, 1)]
        p2 = 0, 0
        is_in = math_utils.point_in_triangle(shape3, p2)
        self.assertEqual(True, is_in)

    def test_rotate_vector(self):
        vector = -1, 1
        vector_degrees = math.degrees(math.atan2(vector[1], vector[0]))
        degrees = 2 * (180 - vector_degrees - (-45))
        result = math_utils.rotate_vector(vector, degrees)
        self.assertEqual((1, -1), result)
        vector = 0, 1
        degrees = -45
        result = math_utils.rotate_vector(vector, degrees)
        self.assertEqual((1, -1), result)


if __name__ == '__main__':
    unittest.main()
