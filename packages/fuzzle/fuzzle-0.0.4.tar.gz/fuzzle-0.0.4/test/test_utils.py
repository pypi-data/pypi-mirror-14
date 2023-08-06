import decimal
import unittest

from exceptions import FuzzleError
from lvars import LinguisticVariable
from utils import feq


class FloatComparisonTestCase(unittest.TestCase):
    """ Tests for the float comparision function. """

    def test_not_equal_but_almost_equal(self):
        """ That two numbers that are not equal are almost equal. """
        x = 0.1
        y = 1.0 - 0.9

        self.assertFalse(x == y)
        self.assertTrue(feq(x, y))

    def test_epsilon(self):
        """ Two different numbers are the same depending on the epsilon. """
        x = 0.5
        y = 0.51

        self.assertFalse(feq(x, y, ε=0.01))
        self.assertTrue(feq(x, y, ε=0.1))
