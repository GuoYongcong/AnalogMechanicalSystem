import unittest
from utils import math_utils


class MyTestCase(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
