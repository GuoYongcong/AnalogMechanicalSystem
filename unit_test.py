import unittest
import mathUtils


class MyTestCase(unittest.TestCase):
    def test_something(self):
        shape1 = [(0, 0), (1, 0), (0, 1)]
        shape2 = [(2, 0), (3, 1), (1, 1)]
        vector = (1, 0)
        p = mathUtils.support(shape1, shape2, vector)
        expected = 0, -1
        self.assertEqual(expected, p)


if __name__ == '__main__':
    unittest.main()
