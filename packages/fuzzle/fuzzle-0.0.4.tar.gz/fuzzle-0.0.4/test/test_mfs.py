import unittest
import unittest.mock

import mfs
import operators
from exceptions import OutOfIntervalError, BadOrderError, \
    IndeterminateValueError, UnexpectedTypeError


class MembershipFunctionTestCase(unittest.TestCase):
    """ Tests for base membership functions behavior. """

    def test_wrong_interval_for_output(self):
        """ Checks out-of-range values in membership functions. """

        class MockMf(mfs.MembershipFunction):
            def __init__(self, f_x):
                self.f_x = f_x

            def f(self, x):
                return self.f_x

        wrong_values = -100, -1, -0.0000000001, 1.00000000001, 2, 100,
        for x in wrong_values:
            with self.assertRaises(OutOfIntervalError):
                MockMf(x)(x)


class RectMFTestCase(unittest.TestCase):
    """ Tests for rectangular membership functions. """

    def test_bad_order_in_params_leads_to_error(self):
        """ Initializing with a non monotonic sequence leads to an error. """
        with self.assertRaises(BadOrderError):
            mfs.RectMF(2, 1)

    def test_outer_values(self):
        """ Values out of the definition has a value of 0. """
        mf = mfs.RectMF(-1, 1)
        for x in (-10, -2, -1.00000000000001, 1.00000000000001, 2, 10):
            self.assertAlmostEqual(0, mf(x))
            self.assertNotAlmostEqual(1, mf(x))

    def test_inner_values(self):
        """ Values in the definition has a value of 1. """
        mf = mfs.RectMF(-1, 1)
        for x in (-1, -0.9999999999999, -0.5, 0, 0.5, 0.9999999999999, 1):
            self.assertAlmostEquals(1, mf(x))
            self.assertNotAlmostEquals(0, mf(x))


class TriMFTestCase(unittest.TestCase):
    """ Tests for triangular membership functions. """

    def test_bad_order_in_params_leads_to_error(self):
        """ Initializing with a non monotonic sequence leads to an error. """
        wrong_values = (
            (1, 3, 2),
            (2, 1, 3),
            (2, 3, 1),
            (3, 1, 2),
            (3, 2, 1),
        )
        for a, b, c in wrong_values:
            with self.assertRaises(BadOrderError):
                mfs.TriMF(a, b, c)

    def test_outer_values_in_normal_triangle(self):
        """ Values out of the definition has a value of 0. """
        mf = mfs.TriMF(-1, 0, 1)
        for x in (-10, -2, -1.00000000000001, 1.00000000000001, 2, 10):
            self.assertAlmostEquals(0, mf(x))
            self.assertNotAlmostEquals(1, mf(x))

    def test_outer_values_in_right_triangles(self):
        """ Values out of the definition has a value of 0. """
        for mf in (mfs.TriMF(-1, 1, 1), mfs.TriMF(-1, -1, 1)):
            for x in (-10, -2, -1.00000000000001, 1.00000000000001, 2, 10):
                self.assertAlmostEquals(0, mf(x))
                self.assertNotAlmostEquals(1, mf(x))

    def test_outer_values_in_spike_triangle(self):
        """ Values out of the definition has a value of 0. """
        mf = mfs.TriMF(0, 0, 0)
        for x in (-10, -1, -0.00000000000001, 0.00000000000001, 1, 10):
            self.assertAlmostEquals(0, mf(x))
            self.assertNotAlmostEquals(1, mf(x))

    def test_inner_values_in_normal_triangle(self):
        """ Values in the definition has a value distinct of 0. """
        mf = mfs.TriMF(-1, 0, 1)
        for x, y in ((0, 1), (0.5, 0.5), (-0.5, 0.5)):
            self.assertAlmostEquals(y, mf(x))

    def test_inner_values_in_right_triangles(self):
        """ Values in the definition has a value distinct of 0. """
        mf1 = mfs.TriMF(-1, 1, 1)
        mf2 = mfs.TriMF(-1, -1, 1)
        values = (
            (mf1, -0.5, 0.25),
            (mf1, 0, 0.5),
            (mf1, 0.5, 0.75),
            (mf1, 1, 1),
            (mf2, -1, 1),
            (mf2, -0.5, 0.75),
            (mf2, 0, 0.5),
            (mf2, 0.5, 0.25),
        )
        for mf, x, y in values:
            self.assertAlmostEquals(y, mf(x))

# TODO De aquí para abajo más tests!
class TrapMFTestCase(unittest.TestCase):
    """ Tests for trapezoidal membership functions. """

    def test_bad_order_in_params_leads_to_error(self):
        """ Initializing with a non monotonic sequence leads to an error. """
        wrong_values = (
            (1, 2, 4, 3),
            (1, 3, 2, 4),
            (1, 3, 4, 2),
            (1, 4, 2, 3),
            (1, 4, 3, 2),
            (2, 1, 3, 4),
            (2, 1, 4, 3),
            (2, 3, 1, 4),
            (2, 3, 4, 1),
            (2, 4, 1, 3),
            (2, 4, 3, 1),
            (3, 1, 2, 4),
            (3, 1, 4, 2),
            (3, 2, 1, 4),
            (3, 2, 4, 1),
            (3, 4, 1, 2),
            (3, 3, 2, 1),
            (4, 1, 2, 3),
            (4, 1, 3, 2),
            (4, 2, 1, 3),
            (4, 2, 3, 1),
            (4, 3, 1, 2),
            (4, 3, 2, 1),
        )
        for a, b, c, d in wrong_values:
            with self.assertRaises(BadOrderError):
                mfs.TrapMF(a, b, c, d)


class SlopeMFTestCase(unittest.TestCase):
    """ Tests for line membership functions. """
    pass


class LineAscMFTestCase(unittest.TestCase):
    """ Tests for ascendent line membership functions. """

    def test_bad_order_in_params_leads_to_error(self):
        """ Initializing with a non monotonic sequence leads to an error. """
        with self.assertRaises(BadOrderError):
            mfs.LineAscMF(2, 1)


class LineDescMFTestCase(unittest.TestCase):
    """ Tests for descendent line membership functions. """

    def test_bad_order_in_params_leads_to_error(self):
        """ Initializing with a non monotonic sequence leads to an error. """
        with self.assertRaises(BadOrderError):
            mfs.LineDescMF(2, 1)


class SingletonMFTestCase(unittest.TestCase):
    """ Tests for singleton membership functions. """
    pass


class GaussMFTestCase(unittest.TestCase):
    """ Tests for normal (gauss) membership functions. """

    def test_standard_deviation_cannot_be_0(self):
        """ An invalid standard deviation leads to an error. """
        with self.assertRaises(IndeterminateValueError):
            mfs.GaussMF(1, 0)


class LogisticMFTestCase(unittest.TestCase):
    """ Tests for a logistic membership functions. """
    pass


class CompositeMFTestCase(unittest.TestCase):
    """ Tests for composite membership functions. """

    def test_wrong_types_for_mfs(self):
        """ Initialization params should be membership functions. """
        wrong_values = (
            (mfs.SingletonMF(1), 1),
            (1, mfs.SingletonMF(1)),
            (1, 1),
        )
        for g in wrong_values:
            for f in wrong_values:
                with self.assertRaises(UnexpectedTypeError):
                    mfs.CompositeMF(g, f)


class ConstantMFTestCase(unittest.TestCase):
    """ Tests for constant membership functions. """

    def test_constant_mf_cannot_return_outside_of_0_1(self):
        """ The return value should belong to the interval [0, 1]. """
        wrong_values = -100, -1, -0.0000000001, 1.00000000001, 2, 100,
        for x in wrong_values:
            with self.assertRaises(OutOfIntervalError):
                mfs.ConstantMF(x)


class BinOpMFTestCase(unittest.TestCase):
    """ Tests for binary operation membership functions. """

    def test_wrong_types_for_norm(self):
        """ binary_op param should be a Norm instance. """
        wrong_values = 'Maximum', max, (1, 2, 3), [1, 2, 3], mfs.ConstantMF(1)
        for x in wrong_values:
            with self.assertRaises(UnexpectedTypeError):
                mfs.BinOpMF(x, mfs.ConstantMF(1), mfs.ConstantMF(1))

    def test_wrong_types_for_mfs(self):
        """ Params f and g should be MembershipFunction instances. """
        wrong_values = 'TriMF', max, 1000, (1, 2, 3), operators.Maximum
        for f in wrong_values:
            for g in wrong_values:
                with self.assertRaises(UnexpectedTypeError):
                    mfs.BinOpMF(operators.Maximum, f, g)
