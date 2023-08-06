import pickle
import unittest

from tempfile import TemporaryFile

from pynetics.replacements import LowElitism, HighElitism
from test import utils


class LowElitismTestCase(unittest.TestCase):
    """ Tests for low elitism replacement method. """

    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(LowElitism(), f)

    def test_replacement_maintains_population_size(self):
        size = 10
        population = utils.DummyPopulation(size=size)
        offsprings = (utils.individuals(i) for i in range(size))

        replacement = LowElitism()
        for offspring in offsprings:
            pre_length = len(population)
            replacement(population, offspring)
            self.assertEquals(pre_length, len(population))


class HighElitismTestCase(unittest.TestCase):
    """ Tests for low elitism replacement method. """

    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(LowElitism(), f)

    def test_replacement_maintains_population_size(self):
        size = 10
        population = utils.DummyPopulation(size=size)
        offsprings = (utils.individuals(i) for i in range(size))

        replacement = HighElitism()
        for offspring in offsprings:
            pre_length = len(population)
            replacement(population, offspring)
            self.assertEquals(pre_length, len(population))
