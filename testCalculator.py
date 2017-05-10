import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_cubicWeight_given_40_20_30_glob_return_6000(self):
        self.assertAlmostEqual(self.calc.cubicWeight (40, 20, 30), 6000, 2)

    def test_cubicWeight_given_26_5_26_glob_return_845(self):
        self.assertAlmostEqual(self.calc.cubicWeight (26, 5, 26), 845, 2)

if __name__ == '__main__':
    unittest.main()
