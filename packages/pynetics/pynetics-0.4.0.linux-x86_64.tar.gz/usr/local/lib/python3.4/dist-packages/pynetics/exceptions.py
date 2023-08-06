class PyneticsError(Exception):
    """ Base class for the errors raised in pynetics library. """
    pass


class InvalidSize(PyneticsError):
    """ Raised when an instance is not of the expected class. """

    def __init__(self, expected, current):
        """ Initializes the exception.

        :param expected: The expected size.
        :param current: The current size.
        """
        super().__init__('Expected {} but got {}'.format(expected, current))


class WrongValueForInterval(ValueError):
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


class NotAProbabilityError(WrongValueForInterval):
    """ If a value is not a valid probability. """

    def __init__(self, var_name, value):
        """ Initializes the instance.

        :param var_name: The variable name which contains the wrong value.
        :param value: The value.
        """
        super().__init__(var_name, 0, 1, value, inc_lower=True, inc_upper=True)
