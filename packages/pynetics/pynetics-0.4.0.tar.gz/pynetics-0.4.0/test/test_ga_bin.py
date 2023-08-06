import pickle
from unittest import TestCase

from tempfile import TemporaryFile

from pynetics.ga_bin import binary_alleles, BinaryIndividualSpawningPool, \
    GeneralizedRecombination
from test import utils


class BinaryAllelesTestCase(TestCase):
    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(binary_alleles, f)

    def test_binary_alleles_only_contains_0_and_1(self):
        self.assertEquals(len(binary_alleles.symbols), 2)
        self.assertIn(0, binary_alleles.symbols)
        self.assertIn(1, binary_alleles.symbols)


class BinaryIndividualSpawningPoolTestCase(TestCase):
    """ Tests for instances of this class. """

    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(BinaryIndividualSpawningPool(
                10,
                utils.DummyFitness()
            ), f)


class GeneralizedRecombinationTestCase(TestCase):
    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(GeneralizedRecombination(), f)
