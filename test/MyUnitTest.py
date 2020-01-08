import math
import unittest

from utils import math_utils


class MyTestCase(unittest.TestCase):

    def test_rotate_vector(self):
        vector = 0, -1
        expected = 0, -1
        degrees = -45
        result = math_utils.rotate_vector(vector, degrees)
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
