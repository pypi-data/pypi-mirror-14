import unittest
import unittest.mock

import operators
from exceptions import OutOfIntervalError


class ComplementTestCase(unittest.TestCase):
    """ Tests for base complement behavior. """

    def setUp(self):
        """ Initializes some values for the tests. """
        self.complement_classes = (
            operators.Zadeh(),
            operators.Sugeno(a=0.5),
            operators.Yager(a=0.5),
        )

    def test_wrong_interval_for_input(self):
        """ The name cannot be other than a non empty string. """
        wrong_values = -1, -0.000000000001, 1.000000000001, 2
        for complement in self.complement_classes:
            with self.assertRaises(OutOfIntervalError):
                [complement(x) for x in wrong_values]

    def test_wrong_interval_for_output(self):
        """ Checks out-of-range values in the complement methods. """

        class MockComplement(operators.Complement):
            def f(self, x):
                return abs(x) + 2

        with self.assertRaises(OutOfIntervalError):
            MockComplement()(1)


class ZadehTestCase(unittest.TestCase):
    """ Tests for the Zadeh's complement operator. """

    def test_correct_implementation(self):
        values = [x / 10. for x in range(1, 10)]
        diffs = [1. - x for x in values]
        complement = operators.Zadeh()
        for value, diff in zip(values, diffs):
            self.assertAlmostEqual(diff, complement(value))

    def test_valid_a(self):
        values_for_x = [x / 10. for x in range(1, 10)]
        f = operators.Zadeh()
        for x in values_for_x:
            self.assertIsInstance(f(x), float)


class SugenoTestCase(unittest.TestCase):
    """ Tests for the Sugeno's complement operator. """

    def test_wrong_a(self):
        """ Alpha value should belong to the [0, 1] interval. """
        wrong_values = -1, -0.000000000001, 1.000000000001, 2
        with self.assertRaises(OutOfIntervalError):
            [operators.Sugeno(x) for x in wrong_values]

    def test_valid_a(self):
        values_for_x = [x / 10. for x in range(1, 10)]
        values_for_a = [x / 10. for x in range(1, 10)]
        for a in values_for_a:
            f = operators.Sugeno(a)
            for x in values_for_x:
                self.assertIsInstance(f(x), float)


class YagerTestCase(unittest.TestCase):
    """ Tests for the Sugeno's complement operator. """

    def test_wrong_a(self):
        """ Alpha value should belong to the [0, 1] interval. """
        wrong_values = -1, -0.000000000001, 1.000000000001, 2
        with self.assertRaises(OutOfIntervalError):
            [operators.Yager(x) for x in wrong_values]

    def test_valid_a(self):
        values_for_x = [x / 10. for x in range(1, 10)]
        values_for_a = [x / 10. for x in range(1, 10)]
        for a in values_for_a:
            f = operators.Yager(a)
            for x in values_for_x:
                self.assertIsInstance(f(x), float)


class NormTestCase(unittest.TestCase):
    """ Tests for base norm behavior. """

    def setUp(self):
        """ Initializes some values for the tests. """
        self.norm_classes = (
            operators.ArithmeticMean(),
            operators.GeometricMean(),
            operators.Minimum(),
            operators.AlgebraicProduct(),
            operators.DrasticProduct(),
            operators.BoundedDifference(),
            operators.DombiTNorm(1),
            operators.EinsteinTNorm(),
            operators.HamacherTNorm(),
            operators.YagerTNorm(1),
            operators.Maximum(),
            operators.AlgebraicSum(),
            operators.BoundedSum(),
            operators.DrasticSum(),
            operators.DombiSNorm(1),
            operators.EinsteinSNorm(),
            operators.HamacherSNorm(),
            operators.YagerSNorm(1),
        )

    def test_wrong_interval_for_input(self):
        """ The name cannot be other than a non empty string. """
        wrong_values = -1, -0.000000000001, 1.000000000001, 2
        valid_values = [x / 10. for x in range(1, 10)]
        for norm in self.norm_classes:
            with self.assertRaises(OutOfIntervalError):
                for x in valid_values:
                    for y in wrong_values:
                        norm(x, y)
                        norm(y, x)
                for x in wrong_values:
                    for y in wrong_values:
                        norm(x, y)
                        norm(y, x)

    def test_wrong_interval_for_output(self):
        """ Checks out-of-range values in the complement methods. """

        class MockNorm(operators.Complement):
            def f(self, x):
                return abs(x) + 2

        with self.assertRaises(OutOfIntervalError):
            MockNorm()(1)


class ArithmeticMeanTestCase(unittest.TestCase):
    """ Tests for the Arithmetic Mean operator. """

    def test_valid_a(self):
        values = [x / 10. for x in range(1, 10)]
        f = operators.ArithmeticMean()
        for x in values:
            for y in values:
                self.assertIsInstance(f(x, y), float)


class GeometricMeanTestCase(unittest.TestCase):
    """ Tests for the Geometric Mean operator. """

    def test_valid_a(self):
        values = [x / 10. for x in range(1, 10)]
        f = operators.GeometricMean()
        for x in values:
            for y in values:
                self.assertIsInstance(f(x, y), float)


class MinimumTestCase(unittest.TestCase):
    """ Tests for the Minimum operator. """

    def test_valid_a(self):
        values = [x / 10. for x in range(1, 10)]
        f = operators.Minimum()
        for x in values:
            for y in values:
                self.assertIsInstance(f(x, y), float)


class AlgebraicProductTestCase(unittest.TestCase):
    """ Tests for the Algebraic Product operator. """

    def test_valid_a(self):
        values = [x / 10. for x in range(1, 10)]
        f = operators.AlgebraicProduct()
        for x in values:
            for y in values:
                self.assertIsInstance(f(x, y), float)


class DrasticProductTestCase(unittest.TestCase):
    """ Tests for the Drastic Product operator. """

    def test_valid_a(self):
        values = [x / 10. for x in range(1, 10)]
        f = operators.DrasticProduct()
        for x in values:
            for y in values:
                self.assertIsInstance(f(x, y), float)


class BoundedDifferenceTestCase(unittest.TestCase):
    """ Tests for the Bounded Difference operator. """

    def test_valid_a(self):
        values = [x / 10. for x in range(1, 10)]
        f = operators.BoundedDifference()
        for x in values:
            for y in values:
                self.assertIsInstance(f(x, y), float)


class DombiTNormTestCase(unittest.TestCase):
    """ Tests for the Dombi t-norm operator. """

    def test_wrong_p(self):
        """ The p parameter should belong to the [0, ∞) interval. """
        wrong_values = -1000, -1, -0.000000000001,
        with self.assertRaises(OutOfIntervalError):
            [operators.DombiTNorm(p) for p in wrong_values]

    def test_with_valid_p(self):
        input_values = [x / 10. for x in range(1, 10)]
        values_for_p = [x / 10. for x in range(1, 100, 3)]
        for p in values_for_p:
            f = operators.DombiTNorm(p)
            for x in input_values:
                for y in input_values:
                    self.assertIsInstance(f(x, y), float)


class EinsteinTNormTestCase(unittest.TestCase):
    """ Tests for the Einstein t-norm operator. """

    def test_valid_a(self):
        values = [x / 10. for x in range(1, 10)]
        f = operators.EinsteinTNorm()
        for x in values:
            for y in values:
                self.assertIsInstance(f(x, y), float)


class HamacherTNormTestCase(unittest.TestCase):
    """ Tests for the Hamacher t-norm operator. """

    def test_valid_a(self):
        values = [x / 10. for x in range(1, 10)]
        f = operators.HamacherTNorm()
        for x in values:
            for y in values:
                self.assertIsInstance(f(x, y), float)


class YagerTNormTestCase(unittest.TestCase):
    """ Tests for the Yager t-norm operator. """

    def test_wrong_p(self):
        """ The p parameter should belong to the [0, ∞) interval. """
        wrong_values = -1000, -1, -0.000000000001,
        with self.assertRaises(OutOfIntervalError):
            [operators.YagerTNorm(p) for p in wrong_values]

    def test_with_valid_p(self):
        input_values = [x / 10. for x in range(1, 10)]
        values_for_p = [x / 10. for x in range(1, 100, 3)]
        for p in values_for_p:
            f = operators.YagerTNorm(p)
            for x in input_values:
                for y in input_values:
                    self.assertIsInstance(f(x, y), float)


class MaximumTestCase(unittest.TestCase):
    """ Tests for the Maximum operator. """

    def test_valid_a(self):
        values = [x / 10. for x in range(1, 10)]
        f = operators.Maximum()
        for x in values:
            for y in values:
                self.assertIsInstance(f(x, y), float)


class AlgebraicSumTestCase(unittest.TestCase):
    """ Tests for the Algebraic Sum operator. """

    def test_valid_a(self):
        values = [x / 10. for x in range(1, 10)]
        f = operators.AlgebraicSum()
        for x in values:
            for y in values:
                self.assertIsInstance(f(x, y), float)


class BoundedSumTestCase(unittest.TestCase):
    """ Tests for the Bounded Sum operator. """

    def test_valid_a(self):
        values = [x / 10. for x in range(1, 10)]
        f = operators.BoundedSum()
        for x in values:
            for y in values:
                self.assertIsInstance(f(x, y), float)


class DrasticSumTestCase(unittest.TestCase):
    """ Tests for the Drastic Sum operator. """

    def test_valid_a(self):
        values = [x / 10. for x in range(1, 10)]
        f = operators.DrasticSum()
        for x in values:
            for y in values:
                self.assertIsInstance(f(x, y), float)


class DombiSNormTestCase(unittest.TestCase):
    """ Tests for the Dombi s-norm operator. """

    def test_wrong_p(self):
        """ The p parameter should belong to the [0, ∞) interval. """
        wrong_values = -1000, -1, -0.000000000001,
        with self.assertRaises(OutOfIntervalError):
            [operators.DombiSNorm(p) for p in wrong_values]

    def test_with_valid_p(self):
        input_values = [x / 10. for x in range(1, 10)]
        values_for_p = [x / 10. for x in range(1, 100, 3)]
        for p in values_for_p:
            f = operators.DombiSNorm(p)
            for x in input_values:
                for y in input_values:
                    self.assertIsInstance(f(x, y), float)


class EinsteinSNormTestCase(unittest.TestCase):
    """ Tests for the Einstein s-norm operator. """

    def test_valid_a(self):
        values = [x / 10. for x in range(1, 10)]
        f = operators.EinsteinSNorm()
        for x in values:
            for y in values:
                self.assertIsInstance(f(x, y), float)


class HamacherSNormTestCase(unittest.TestCase):
    """ Tests for the Hamacher s-norm operator. """

    def test_valid_a(self):
        values = [x / 10. for x in range(1, 10)]
        f = operators.HamacherSNorm()
        for x in values:
            for y in values:
                self.assertIsInstance(f(x, y), float)


class YagerSNormTestCase(unittest.TestCase):
    """ Tests for the Yager s-norm operator. """

    def test_wrong_p(self):
        """ The p parameter should belong to the [0, ∞) interval. """
        wrong_values = -1000, -1, -0.000000000001,
        with self.assertRaises(OutOfIntervalError):
            [operators.YagerSNorm(p) for p in wrong_values]

    def test_with_valid_p(self):
        input_values = [x / 10. for x in range(1, 10)]
        values_for_p = [x / 10. for x in range(1, 100, 3)]
        for p in values_for_p:
            f = operators.YagerSNorm(p)
            for x in input_values:
                for y in input_values:
                    self.assertIsInstance(f(x, y), float)
