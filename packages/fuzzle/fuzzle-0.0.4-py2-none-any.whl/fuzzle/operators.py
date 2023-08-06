import math

import abc

from fuzzle.exceptions import OutOfIntervalError


# TODO Better comments
# TODO More operators. See https://en.wikipedia.org/wiki/Construction_of_t-norms

class Operator(metaclass=abc.ABCMeta):
    """ Represents all possible fuzzy operators.

    This operators will work in the [0, 1] ⊆ ℝ domain. They include both unary
    (complements) and binary (t-norms and s-norms).
    """


class Complement(Operator, metaclass=abc.ABCMeta):
    """ Interface for all complement operators. """

    def __call__(self, x):
        """ Performs the operation.

        :param x: A value that should belong to the real interval [0, 1].
        :return: The complement of the value according to the chosen complement
            implementation.
        """
        if not 0. <= x <= 1.:
            raise OutOfIntervalError('x', 0, 1, x)

        f_x = self.f(float(x))
        if not 0. <= f_x <= 1.:
            raise OutOfIntervalError('f(x)', 0, 1, f_x)
        return float(f_x)

    @abc.abstractmethod
    def f(self, x):
        """ The concrete implementation of the complement method.

        :param x: The value with which operate.
        :return: The computed complement.
        """


class Zadeh(Complement):
    """ Zadeh's complement, defined as f(x) = 1 - x. """

    def f(self, x):
        return 1 - x


class Sugeno(Complement):
    """ Sugeno's complement for a scalar "a".

    If a = 0 then Sugeno's complement is equivalent to Zadeh's complement.
    """

    def __init__(self, a):
        if not 0 <= a <= 1:
            raise OutOfIntervalError('a', 0, 1, a)

        self.a = float(a)

    def f(self, x):
        return (1 - x) / (1 + x * self.a)


class Yager(Complement):
    """ Yager's complement for a scalar "a".

    If a = 1 then Yager's complement is equivalent to Zadeh's complement.
    """

    def __init__(self, a):
        if not 0 <= a <= 1:
            raise OutOfIntervalError('a', 0, 1, a)

        self.a = float(a)
        self.__inv_a = 1. / self.a

    def f(self, x):
        return pow(1. - pow(x, self.a), self.__inv_a)


class Norm(Operator, metaclass=abc.ABCMeta):
    """ Interface for all norms (t-norm and t-conorm) operations. """

    def __call__(self, x, y):
        """ Performs the operation.

        :param x: A value that should belong to the real interval [0, 1].
        :return: The complement of the value according to the chosen complement
            implementation.
        """
        if not 0. <= x <= 1.:
            raise OutOfIntervalError('x', 0, 1, x)
        if not 0. <= y <= 1.:
            raise OutOfIntervalError('y', 0, 1, y)

        f_x_y = self.f(float(x), float(y))
        if not 0. <= f_x_y <= 1.:
            raise OutOfIntervalError('f(x, y)', 0, 1, f_x_y)
        return float(f_x_y)

    @abc.abstractmethod
    def f(self, x, y):
        """ The concrete implementation of a Norm.

        :param x: One of the values with which operate.
        :param y: One of the values with which operate.
        :return: The computed norm.
        """


class TNorm(Norm, metaclass=abc.ABCMeta):
    """Interface for all T-Norm operators."""
    pass


class SNorm(Norm, metaclass=abc.ABCMeta):
    """Interface for all S-Norm operators."""
    pass


class ArithmeticMean(TNorm):
    """ The midpoint of two given values. """

    def f(self, x, y):
        return (x + y) / 2.


class GeometricMean(TNorm):
    """ The squared of the product of two given values. """

    def f(self, x, y):
        return math.sqrt(x * y)


class Minimum(TNorm):
    """ Minimum of two given values. """

    def f(self, x, y):
        return min(x, y)


class AlgebraicProduct(TNorm):
    """ Algebraic product.

    The common product of two values.
    """

    def f(self, x, y):
        return x * y


class DrasticProduct(TNorm):
    """ Drastic product. """

    def f(self, x, y):
        if x == 1:
            return y
        elif y == 1:
            return x
        else:
            return 0


class BoundedDifference(TNorm):
    """ The bounded difference returns x - y if x > y or 0 otherwise. """

    def f(self, x, y):
        return max(0., x - y)


class DombiTNorm(TNorm):
    """ Dombi T-Norm. """

    def __init__(self, p):
        if p < 0:
            raise OutOfIntervalError('p', 0, '∞', p, inc_upper=False)

        self.p = float(p)
        self.__inv_p = 1 / self.p

    def f(self, x, y):
        if x == 0 or y == 0:
            return 0.
        else:
            def λ(z):
                return pow((1 - z) / z, self.p)

            return 1 / (1 + pow(λ(x) + λ(y), self.__inv_p))


class EinsteinTNorm(TNorm):
    """ Einstein T-Norm. """

    def f(self, x, y):
        return (x * y) / (1 + (1 - x) * (1 - y))


class HamacherTNorm(TNorm):
    """Hamacher T-Norm. """

    def f(self, x, y):
        if not x or not y:
            return 0.
        else:
            return (x * y) / (x + y - x * y)


class YagerTNorm(TNorm):
    """Yager T-Norm. """

    def __init__(self, p):
        if p < 0:
            raise OutOfIntervalError('p', 0, '∞', p, inc_upper=False)

        self.p = float(p)
        self.__inv_p = 1 / self.p

    def f(self, x, y):
        if x == 0. or y == 0.:
            return 0.
        else:
            def λ(z):
                return pow(1 - z, self.p)

            return 1 - min(1, pow(λ(x) + λ(y), self.__inv_p))


class Maximum(SNorm):
    """ Maximum of two given values. """

    def f(self, x, y):
        return max(x, y)


class AlgebraicSum(SNorm):
    """ The sum of two given values minus their product. """

    def f(self, x, y):
        return x + y - x * y


class BoundedSum(SNorm):
    """ The sum of two given values bounded above by 1. """

    def f(self, x, y):
        return min(1, x + y)


class DrasticSum(SNorm):
    """ Drastic sum. """

    def f(self, x, y):
        if not x:
            return y
        elif not y:
            return x
        else:
            return 1


class DombiSNorm(SNorm):
    """Dombi's t-conorm. """

    def __init__(self, p):
        if p < 0:
            raise OutOfIntervalError('p', 0, '∞', p, inc_upper=False)

        self.p = float(p)
        self.__inv_p = 1 / self.p

    def f(self, x, y):
        if x == 1 or y == 1:
            return 1
        else:
            def λ(z):
                return pow(x / (1. - z), self.p)

            return 1 - 1 / (1 + pow(λ(x) + λ(y), self.__inv_p))


class EinsteinSNorm(SNorm):
    """ Einstein's t-conorm. """

    def f(self, x, y):
        return (x + y) / (1 + x * y)


class HamacherSNorm(SNorm):
    """ Hamacher's t-conorm. """

    def f(self, x, y):
        if x == y == 1.:
            return 1
        else:
            return (x + y - 2 * x * y) / (1 - x * y)


class YagerSNorm(SNorm):
    """Yager's t-conorm. """

    def __init__(self, p):
        if p < 0:
            raise OutOfIntervalError('p', 0, '∞', p, inc_upper=False)

        self.p = float(p)
        self.__inv_p = 1 / self.p

    def f(self, x, y):
        if x == y == 1:
            return 1
        else:
            def λ(z):
                return pow(z, self.p)

            return min(1, pow(λ(x) + λ(y), self.__inv_p))
