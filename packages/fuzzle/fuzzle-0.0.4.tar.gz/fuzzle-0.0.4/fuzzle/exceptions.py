class FuzzleError(Exception):
    """ Base exception for all library related errors. """
    pass


class OutOfIntervalError(FuzzleError):
    """ When a value does not belong to an interval. """

    def __init__(
            self,
            var_name,
            lower,
            upper,
            value,
            inc_lower=True,
            inc_upper=True,
    ):
        """ Initializes the exception.

        :param var_name: The variable name which contains the wrong value.
        :param lower: The lower bound of the interval.
        :param upper: The upper bound of the interval.
        :param value: The value.
        :param inc_lower: If the lower bound is include. Defaults to True.
        :param inc_upper: If the upper bound is include. Defaults to True.
        """
        self.lower = lower
        self.upper = upper
        self.var_name = var_name
        self.value = value
        self.inc_lower = inc_lower
        self.inc_upper = inc_upper
        msg = 'Expected {} ∈ {}{}, {}{} but got {}'.format(
                var_name,
                '[' if inc_lower else '(',
                self.lower,
                self.upper,
                ']' if inc_upper else ')',
                self.value,
        )
        super().__init__(msg)


class BadOrderError(FuzzleError):
    """ When a list of values are expected in an ordered way. """

    def __init__(self, *args):
        super().__init__('Bad order: {}'.format(
                ' <= '.join((str(x) for x in args)))
        )


class IndeterminateValueError(FuzzleError):
    """ When a value in a veriable leads to an indeterminate value. """

    def __init__(self, var, value):
        super().__init__('{} = {}'.format(var, value))


class UnexpectedTypeError(FuzzleError):
    """ When a value has an unexpected type. """

    def __init__(self, var, t):
        super().__init__('Variable {} must be of type {}'.format(var, t))


class ParseError(FuzzleError):
    """ When there was an error parsing something. """

    def __init__(self, exp, real, value=None):
        msg = 'Expected {}, but {} found'.format(exp, real)
        if value is not None:
            msg = ' ("{}")'.format(value)
        super().__init__(msg)
