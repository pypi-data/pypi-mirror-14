import pickle
from unittest import TestCase

from tempfile import TemporaryFile

from pynetics.ga_real import RealIntervalAlleles, MorphologicalRecombination


class RealIntervalAllelesTestCase(TestCase):
    """ Tests for instances of the base class Alleles. """

    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(RealIntervalAlleles(0, 1), f)

    def test_bounds_are_correctly_stored_after_initialization(self):
        bounds = [0, 1]
        self.assertEquals(RealIntervalAlleles(*bounds).a, min(bounds))
        self.assertEquals(RealIntervalAlleles(*bounds).b, max(bounds))
        bounds.reverse()
        self.assertEquals(RealIntervalAlleles(*bounds).a, min(bounds))
        self.assertEquals(RealIntervalAlleles(*bounds).b, max(bounds))


class MorphologicalRecombinationTestCase(TestCase):
    """ Tests for instances of the class FiniteSetAlleles. """

    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(MorphologicalRecombination(), f)
