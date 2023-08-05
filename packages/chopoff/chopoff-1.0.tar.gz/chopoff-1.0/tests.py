import unittest
from chopoff.chopoff import chopoff


class ChopTest(unittest.TestCase):
    def setUp(self):
        self.sample = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_chopoff_one(self):
        self.assertEqual([1, 2, 3], chopoff([3], self.sample))

    def test_chopoff_two(self):
        self.assertEqual([1, 2, 3, 4, 5, 9, 10], chopoff([5, 8], self.sample))

    def test_chopoff_three(self):
        self.assertEqual([1, 2, 3, 5, 7, 9, 10], chopoff([3, 8, 2], self.sample))

    def test_chopoff_equal(self):
        self.assertEqual([], chopoff([3, 3, 2], self.sample))

    def test_chopoff_three_negative(self):
        self.assertEqual([], chopoff([3, 8, -2], self.sample))


if __name__ == '__main__':
    unittest.main()
