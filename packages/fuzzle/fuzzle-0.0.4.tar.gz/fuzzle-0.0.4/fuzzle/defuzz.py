import numbers

import abc

from fuzzle.exceptions import UnexpectedTypeError, FuzzleError
from fuzzle.lvars import LinguisticVariable
from fuzzle.mfs import MembershipFunction
from fuzzle.utils import frange, feq


class DefuzzificationMethod(metaclass=abc.ABCMeta):
    """ Represents a defuzzification operator. """

    def __init__(self, resolution=None):
        """ Initializes the instance.

        :param resolution: The number of point the domain should be partitioned
            in order to get the result.
        """
        self.resolution = float(resolution or 0)

    def __call__(self, mf, lvar):
        """ Performs the defuzzification operation.

        :param mf: the membership function to defuzzify.
        :param lvar: the linguistic variable under the fuzzy set defined for
            the membership function.
        :return: A float value with the result of the defuzzifying the function.
        :raises UnexpectedTypeError: If mf is not a MembershipFunction instance
            or if lvar is not a LinguisticVariable Instance.
        """
        if not isinstance(mf, MembershipFunction):
            raise UnexpectedTypeError('mf', MembershipFunction)
        if not isinstance(lvar, LinguisticVariable):
            raise UnexpectedTypeError('lvar', LinguisticVariable)

        f_x = self.f(mf, lvar)

        if not isinstance(f_x, numbers.Number):
            raise FuzzleError('Expected return value to be a numeric value')

        return float(f_x)

    @abc.abstractmethod
    def f(self, mf, l_var):
        """ The method to be overriden in order to apply the function.

        :param mf: A membership function to defuzzify.
        :param l_var: A linguistic variable under the fuzzy se defined for this
            linguistic variable.
        :return: A value with the result of the defuzzifying the function. It
            should be any value representable as a float.
        """


class CoG(DefuzzificationMethod):
    """ Center of gravity method of defuzzification. """

    def __init__(self, resolution=10000):
        """ Initilalizes the instance.

        :param resolution: The number of point the domain should be partitioned
            in order to get the result. The higher the resolution, the more
            precise is the result but the longer the method lasts.
        """
        super().__init__(resolution=resolution)

    def f(self, mf, l_var):
        start, stop = l_var.domain
        step = float(stop - start) / self.resolution

        weighted_sum, total_sum = 0, 0
        for x in frange(start=start, stop=stop, step=step):
            y = mf(x)
            if not feq(y, 0):
                weighted_sum += x * y
                total_sum += y
        return (stop + start) / 2 if feq(total_sum, 0) else weighted_sum / total_sum


class CoGS(DefuzzificationMethod):
    """ Center of gravity method of singleton defuzzification. """

    def f(self, mf, l_var):
        values = [l_var[fset].a for fset in l_var]

        num, den = .0, .0
        for x in values:
            y = mf(x)
            num += y * x
            if y:
                den += y
        return None if den == 0.0 else num / den


class WtSum(DefuzzificationMethod):
    """ Weighted sum of singleton defuzzification. """

    def f(self, mf, l_var):
        values = [l_var[fset].a for fset in l_var]
        return sum([x * mf(x) for x in values])
