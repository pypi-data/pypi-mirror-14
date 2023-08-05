import pickle
from unittest import TestCase
from unittest.mock import Mock

from tempfile import TemporaryFile

from pynetics.stop import StepsNum, FitnessBound


class StepsNumTestCase(TestCase):
    """ Test for the stop condition based on number of iterations. """

    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(StepsNum(steps=10), f)

    def test_criteria_is_not_met_with_fewer_iterations(self):
        stop_condition = StepsNum(2)
        genetic_algorithm = Mock()
        genetic_algorithm.generation = 0
        self.assertFalse(stop_condition(genetic_algorithm))
        genetic_algorithm.generation = 1
        self.assertFalse(stop_condition(genetic_algorithm))

    def test_criteria_is_not_met_with_same_or_more_iterations(self):
        genetic_algorithm = StepsNum(2)
        population = Mock()
        population.generation = 2
        self.assertTrue(genetic_algorithm(population))
        population.generation = 3
        self.assertTrue(genetic_algorithm(population))


class FitnessBoundTestCase(TestCase):
    """ If the genetic algorithm obtained a fine enough individual. """

    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(StepsNum(steps=10), f)

    def test_criteria_is_not_met_with_a_lower_fitness(self):
        stop_condition = FitnessBound(1.0)
        for fitness in (0.0, 0.25, 0.5, 0.75, 0.9, 0.9999999):
            individual = Mock()
            individual.fitness = Mock(return_value=fitness)
            genetic_algorithm = Mock()
            genetic_algorithm.best = Mock(return_value=individual)
            self.assertFalse(stop_condition(genetic_algorithm))

    def test_criteria_is_not_met_with_a_higher_fitness(self):
        stop_condition = FitnessBound(1.0)
        for fitness in (1.0, 1.000000001, 1.25, 1.5, 1.75, 2):
            individual = Mock()
            individual.fitness = Mock(return_value=fitness)
            genetic_algorithm = Mock()
            genetic_algorithm.best = Mock(return_value=individual)
            self.assertTrue(stop_condition(genetic_algorithm))
