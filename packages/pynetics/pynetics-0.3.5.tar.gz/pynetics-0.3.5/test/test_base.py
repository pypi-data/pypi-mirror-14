import pickle
import unittest

from tempfile import TemporaryFile

from pynetics import PyneticsError
from pynetics.exceptions import InvalidSize
from test import utils


class StopConditionTestCase(unittest.TestCase):
    """ Tests for Individual instances. """

    def test_class_is_pickeable(self):
        """ Checks the individual by writing it in a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(utils.DummyStopCondition(), f)


class IndividualTestCase(unittest.TestCase):
    """ Tests for Individual instances. """

    def test_class_is_pickeable(self):
        """ Checks the individual by writing it in a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(utils.DummyIndividual(), f)


class SpawningPoolTestCase(unittest.TestCase):
    """ Tests for SpawningPool instances. """

    def test_class_is_pickeable(self):
        """ Checks is pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(utils.DummySpawningPool(
                fitness=utils.DummyFitness()
            ), f)

    def test_fitness_method_is_correctly_stored_after_initialization(self):
        """ If fitness method is correctly stored in the instance. """
        fitness = utils.DummyFitness()
        spawning_pool = utils.DummySpawningPool(fitness=fitness)
        self.assertIs(fitness, spawning_pool.fitness)

    def test_spawn_individual_assigns_the_fitness_method(self):
        fitness = utils.DummyFitness()
        spawning_pool = utils.DummySpawningPool(fitness=fitness)
        individual = spawning_pool.spawn()
        self.assertIs(fitness, individual.fitness_method)


class TestPopulation(unittest.TestCase):
    """ Test for populations. """

    def test_class_is_pickeable(self):
        """ Checks is pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(utils.DummyPopulation(size=10), f)

    def test_cannot_initialize_a_population_of_size_0_or_less(self):
        for size in (-100, -10, -1, 0):
            with self.assertRaises(InvalidSize):
                utils.DummyPopulation(size=size)

    def test_population_maintain_size_at_initialization_time(self):
        """ Size is kept when initializing.

        That means that, if a population is initializated with size n, it will
        have n individuals, regardless the number of individuals are passed as
        parameter.
        """
        size = 10
        individuals_list = [[], utils.individuals(10), utils.individuals(100)]
        for individuals in individuals_list:
            self.assertEquals(
                size,
                len(utils.DummyPopulation(size=size, individuals=individuals))
            )

    def test_population_length_is_computed_correctly(self):
        sizes = (1, 10, 100, 1000)
        for size in sizes:
            self.assertEquals(size, len(utils.DummyPopulation(size=size)))

    def test_population_shrinks_when_individual_is_removed(self):
        size = 10
        population = utils.DummyPopulation(size=size)
        for i in range(10):
            self.assertEquals(size - i, len(population))
            del population[0]

    def test_individuals_are_correctly_added_to_the_population(self):
        size = 10
        individuals = utils.individuals(size + 1)
        population = utils.DummyPopulation(
            size=size,
            individuals=individuals[:10]
        )
        self.assertEquals(size, len(population))
        population.append(individuals[10])
        self.assertEquals(size + 1, len(population))
        self.assertIn(individuals[10], population)

    def test_best_individuals_are_returned(self):
        size = 10
        individuals = utils.individuals(size)
        population = utils.DummyPopulation(size=size, individuals=individuals)
        self.assertEquals(
            population.best().fitness(),
            individuals[-1].fitness()
        )


class FitnessTestCase(unittest.TestCase):
    """ Tests for SpawningPool instances. """

    def test_class_is_pickeable(self):
        """ Checks is pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(utils.DummyFitness(), f)


class MutationTestCase(unittest.TestCase):
    """ Tests for Mutation instances. """

    def test_class_is_pickeable(self):
        """ Checks is pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(utils.DummyMutation(), f)


class RecombinationTestCase(unittest.TestCase):
    """ Tests for Recombination instances. """

    def test_class_is_pickeable(self):
        """ Checks is pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(utils.DummyRecombination(), f)


class ReplacementTestCase(unittest.TestCase):
    """ Tests for Replacement instances. """

    def test_class_is_pickeable(self):
        """ Checks is pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(utils.DummyReplacement(), f)


class SelectionTestCase(unittest.TestCase):
    """ Tests for Selection instances. """

    def test_class_is_pickeable(self):
        """ Checks is pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(utils.DummySelection(), f)

    def test_error_if_more_selections_than_size_when_not_repetition(self):
        """ When no repetable and requested more individuals than available. """
        population = utils.DummyPopulation(10)
        for i in range(1, 10):
            with self.assertRaises(PyneticsError):
                utils.DummySelection()(population, len(population) + 1)


class CatastropheTestCase(unittest.TestCase):
    """ Tests for Catastrophe instances. """

    def test_class_is_pickeable(self):
        """ Checks is pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(utils.DummyCatastrophe(), f)
