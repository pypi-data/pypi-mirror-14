import numbers

from fuzzle.exceptions import FuzzleError, UnexpectedTypeError
from fuzzle.mfs import MembershipFunction


class LinguisticVariable(dict):
    """ Common behavior for linguistic vars. """

    def __init__(self, name, domain):
        """ Initializes this membership function.

        :param name: The name for this linguistic variable.
        :param domain: The real interval where this function is defined. It
            should be a tuple in the form (number, number).
        :raises FuzzleError: In case of name being None or empty or in case
            domain being other than a tuple of 2 numeric values.
        """
        super().__init__()

        if not name or not isinstance(name, str):
            raise FuzzleError('Name cannot be None or empty.')
        if not isinstance(domain, tuple) or len(domain) != 2:
            raise FuzzleError('Domain must ba a tuple like (a, b)')
        if not all([isinstance(x, numbers.Number) for x in domain]):
            raise FuzzleError('Domain elements must be numbers')

        self.name = name
        self.domain = float(min(domain)), float(max(domain))

    def __setitem__(self, name, mf):
        """ Assigns to the fuzzy set 'name' the membership function 'mf'.

        :param name: the name of the fuzzy set.
        :param mf: the membership function that defines the set.
        :raises UnexpectedTypeError: If the variable mf is not a valid
            membership function.
        """
        if not isinstance(mf, MembershipFunction):
            raise UnexpectedTypeError('mf', MembershipFunction)
        else:
            return super().__setitem__(name, mf)


class InputLVar(LinguisticVariable):
    """ An input linguistic variable for a fuzzy controller. """

    def fuzzify(self, value):
        """ Fuzzifies a value over all the fuzzy sets in the variable.

        The value (which belongs to the domain of the variable) will be applied
        over the membership functions of all the fuzzy sets defined in the input
        variable.

        It's expected to be anything representable as a float. That includes
        strings in the form '42'.

        :param value: The numeric value to fuzzify.
        :returns: A dictionary with the value fuzzified for all the fuzzy sets.
        :raises FuzzleError: In case the value is not representable as a float
            value.
        """
        try:
            return dict([(name, self[name](float(value))) for name in self])
        except (TypeError, ValueError)as e:
            raise FuzzleError(e)


class OutputLVar(LinguisticVariable):
    """ An output linguistic variable for a fuzzy controller."""

    def __init__(self, name, domain, defuzz):
        """ Initializes this linguistic variable.

        :param name: the name of the variable.
        :param domain: the domain of the variable.
        :param defuzz: the operator to defuzzify the values.
        """
        from fuzzle.defuzz import DefuzzificationMethod

        LinguisticVariable.__init__(self, name, domain)

        if not isinstance(defuzz, DefuzzificationMethod):
            raise UnexpectedTypeError('defuzz', DefuzzificationMethod)
        self.defuzz = defuzz

    def defuzzify(self, fuzzy_val):
        return self.defuzz(fuzzy_val, self)
