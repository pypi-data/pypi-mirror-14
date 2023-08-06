import math

import abc

from fuzzle.exceptions import OutOfIntervalError, BadOrderError, \
    IndeterminateValueError, UnexpectedTypeError
from fuzzle.operators import Norm
from fuzzle.utils import feq


class MembershipFunction(metaclass=abc.ABCMeta):
    """ Base class for all the membership functions to use. """

    def __call__(self, x):
        """ Evaluates the value against this membership function.

        Evaluates the membership degree of value x to the fuzzy set defined by
        this membership function. Delegates the behavior to the abstract method
        p.

        :param x: A value to be evaluated.
        :returns: The value evaluated.
        """
        f_x = self.f(float(x))
        if not 0. <= f_x <= 1.:
            raise OutOfIntervalError('f(x)', 0, 1, f_x)
        return float(f_x)

    @abc.abstractmethod
    def f(self, x):
        """ The method to be overridden in order to apply the function.

        :param x: A float value to be evaluated.
        :return: The value evaluated.
        """


class RectMF(MembershipFunction):
    """ Rectangular membership function. """

    def __init__(self, a, b):
        """ Initializes this membership function.

        :param a: Where this membership function changes from 0 to 1.
        :param b: Where this membership function changes from 1 to 0.
        """
        if not a <= b:
            raise BadOrderError(a, b)
        self.a, self.b = float(a), float(b)

    def f(self, x):
        return float(self.a <= x <= self.b)

    def __repr__(self):
        return '{}(a={}, b={})'.format(type(self).__name__, self.a, self.b)


class TriMF(MembershipFunction):
    """ Triangular membership function. """

    def __init__(self, a, b, c):
        """ Initializes this membership function.

        :param a: Where this membership function begins to grow towards 1.
        :param b: Where this membership function is 1.
        :param c: Where this membership function begins to decrease towards 0.
        """
        if not a <= b <= c:
            raise BadOrderError(a, b, c)

        self.a, self.b, self.c = float(a), float(b), float(c)
        self.__b_minus_a = self.b - self.a
        self.__c_minus_b = self.c - self.b

    def f(self, x):
        if self.a <= x <= self.b:
            return (x - self.a) / self.__b_minus_a if self.__b_minus_a else 1
        elif self.b <= x <= self.c:
            return (self.c - x) / self.__c_minus_b if self.__c_minus_b else 1
        else:
            return 0

    def __repr__(self):
        return '{}(a={}, b={}, c={})'.format(
                type(self).__name__,
                self.a,
                self.b,
                self.c
        )


class TrapMF(MembershipFunction):
    """ Trapezoidal membership function."""

    def __init__(self, a, b, c, d):
        """ Initializes this membership function.

        :param a: value where the membership function begins to grow.
        :param b: value where the membership function starts being 1.0.
        :param c: value where the membership function ends being 1.0.
        :param d: value where the membership function starts decreasing.
        """
        if not a <= b <= c <= d:
            raise BadOrderError(a, b, c, d)

        self.a, self.b, self.c, self.d = float(a), float(b), float(c), float(d)
        self.__b_minus_a = self.b - self.a
        self.__d_minus_c = self.d - self.c

    def f(self, x):
        if self.a <= x <= self.b:
            return (x - self.a) / self.__b_minus_a if self.__b_minus_a else 1
        elif self.b <= x <= self.c:
            return 1
        elif self.c <= x <= self.d:
            return (self.d - x) / self.__d_minus_c if self.__d_minus_c else 1
        else:
            return 0

    def __repr__(self):
        return '{}(a={}, b={}, c={}, d={})'.format(
                type(self).__name__,
                self.a,
                self.b,
                self.c,
                self.d,
        )


class SlopeMF(MembershipFunction):
    """ Line membership function (based on slope and independent term)."""

    def __init__(self, m, n):
        """ New line mf. based on its slope (m) and it independent term (n)."""
        self.m, self.n = float(m), float(n)

    def f(self, x):
        return min(max(self.m * x + self.n, 0), 1)

    def __repr__(self):
        return '{}(m={}, n={})'.format(
                type(self).__name__,
                self.m,
                self.n,
        )


class LineAscMF(MembershipFunction):
    """ Ascendent line membership function."""

    def __init__(self, a, b):
        """ Initializes this membership function.

        :param a: value where the membership function begins to grow.
        :param b: value where the membership function starts being 1.0.
        """
        if not a <= b:
            raise BadOrderError(a, b)
        self.a, self.b = float(a), float(b)
        self.__b_minus_a = float(b - a)

    def f(self, x):
        if x < self.a:
            return 0.
        elif self.__b_minus_a == 0:
            return 1
        elif self.a <= x <= self.b:
            return min(1, max(0, (x - self.a) / self.__b_minus_a))
        else:
            return 1.

    def __repr__(self):
        return '{}(a={}, b={})'.format(
                type(self).__name__,
                self.a,
                self.b,
        )


class LineDescMF(MembershipFunction):
    """ Descendent line membership function."""

    def __init__(self, a, b):
        """ Initializes this membership function.

        :param a: value where the membership function begins decreasing.
        :param b: value where the membership function starts being 0.0.
        """
        if not a <= b:
            raise BadOrderError(a, b)
        self.a, self.b = float(a), float(b)
        self.__b_minus_a = float(b - a)

    def f(self, x):
        if x < self.a:
            return 1
        elif self.a <= x <= self.b:
            high = max(0, (self.b - x) / self.__b_minus_a)
            return min(1, high) if self.__b_minus_a else 1
        else:
            return 0

    def __repr__(self):
        return '{}(a={}, b={})'.format(
                type(self).__name__,
                self.a,
                self.b,
        )


class SingletonMF(MembershipFunction):
    """ Singleton membership function."""

    def __init__(self, a):
        """ Initializes this membership function.

        :param a: value where the membership function is 1.0.
        """
        self.a = float(a)

    def f(self, x):
        return 1 if feq(x, self.a) else 0

    def __repr__(self):
        return '{}(a={})'.format(
                type(self).__name__,
                self.a,
        )


class GaussMF(MembershipFunction):
    """ Bell shaped membership function. """

    def __init__(self, μ, σ):
        """ Initializes this membership function.

        :param μ: the average of the gauss function.
        :param σ: the standard deviation of the function.
        """
        if σ == 0:
            raise IndeterminateValueError('σ', σ)
        self.μ = μ
        self.σ = σ
        self.__var = pow(σ, 2)

    def f(self, x):
        return math.exp(-0.5 * (pow(self.μ - x, 2) / self.__var))

    def __repr__(self):
        return '{}(μ={}, σ={})'.format(type(self).__name__, self.μ, self.σ)


class LogisticMF(MembershipFunction):
    """ Logistic membership function. """

    def f(self, x):
        return 1 / (1 + math.exp(-x))

    def __repr__(self):
        return '{}'.format(type(self).__name__)


class CompositeMF(MembershipFunction):
    """ Composite membership function

    Given f(x) and g(x) mfs, it returns (g o f)(x) mf.
    """

    def __init__(self, g, f):
        """ Initializes this membership function.

        :param g: one membership function.
        :param f: the other membership function.
        """
        if not isinstance(g, MembershipFunction):
            raise UnexpectedTypeError('g', MembershipFunction)
        if not isinstance(f, MembershipFunction):
            raise UnexpectedTypeError('f', MembershipFunction)

        self.g = g
        self.f = f

    def f(self, x):
        return self.g(self.f(x))

    def __repr__(self):
        return '{}(g={}, f={})'.format(
                type(self).__name__,
                repr(self.g),
                repr(self.f),
        )


class ConstantMF(MembershipFunction):
    """ Constant membership function

    Given a real value c it returns c for every x.
    """

    def __init__(self, c):
        """ Initializes this membership function.

        :param c: the constant value.
        """
        if not 0 <= c <= 1:
            raise OutOfIntervalError('c', 0, 1, c)
        self.x = float(c)

    def f(self, x):
        return self.x

    def __repr__(self):
        return '{}(c={})'.format(
                type(self).__name__,
                repr(self.x),
        )


class BinOpMF(MembershipFunction):
    def __init__(self, binary_op, f, g):
        """ Initializes this membership function.

        :param binary_op: the binary operation to apply.
        :param f: one membership function.
        :param g: other membership function.
        """
        if not isinstance(binary_op, Norm):
            raise UnexpectedTypeError('binary_op', Norm)
        if not isinstance(f, MembershipFunction):
            raise UnexpectedTypeError('f', MembershipFunction)
        if not isinstance(g, MembershipFunction):
            raise UnexpectedTypeError('g', MembershipFunction)

        self.op = binary_op
        self.mf1 = f
        self.mf2 = g

    def f(self, x):
        return self.op(self.mf1(x), self.mf2(x))

    def __repr__(self):
        return '{}(op={}, f={}, g={})'.format(
                type(self).__name__,
                repr(self.op),
                repr(self.mf1),
                repr(self.mf2),
        )
