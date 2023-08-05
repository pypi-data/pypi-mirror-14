import pickle
from unittest import TestCase

from tempfile import TemporaryFile

from pynetics.ga_int import IntegerIndividualSpawningPool, \
    IntegerRangeRecombination
from test import utils


class IntegerIndividualSpawningPoolTestCase(TestCase):
    """ Tests for instances of this class. """

    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(IntegerIndividualSpawningPool(
                10,
                utils.DummyFitness(),
                0,
                10,
            ), f)

    def test_lower_bound_is_correctly_sored_after_initialization(self):
        for lower in (-10, -5, 0, 5, 10):
            sp = IntegerIndividualSpawningPool(
                10,
                utils.DummyFitness(),
                lower,
                lower + 10
            )
            self.assertEquals(lower, sp.lower)

    def test_upper_bound_is_correctly_sored_after_initialization(self):
        for upper in (-10, -5, 0, 5, 10):
            sp = IntegerIndividualSpawningPool(
                10,
                utils.DummyFitness(),
                upper - 10,
                upper
            )
            self.assertEquals(upper, sp.upper)


class IntegerRangeRecombinationTestCase(TestCase):
    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(IntegerRangeRecombination(), f)
