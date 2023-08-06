import pickle
from unittest import TestCase

from tempfile import TemporaryFile

from pynetics import PyneticsError
from pynetics.selections import BestIndividual, Tournament
from test import utils


class BestIndividualTestCase(TestCase):
    """ Tests for BestIndividual selection method. """

    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(BestIndividual(), f)

    def test_when_population_size_is_lower_than_selection_size(self):
        """ Cannot select more individuals than population size. """
        p_size = 10
        population = utils.DummyPopulation(size=p_size)

        with self.assertRaises(PyneticsError):
            BestIndividual()(population, p_size * 2)

    def test_when_population_size_is_equals_to_selection_size(self):
        """ All the population is returned. """
        p_size = 10
        individuals = utils.individuals(p_size)
        population = utils.DummyPopulation(size=p_size, individuals=individuals)
        selected_individuals = BestIndividual()(population, p_size)
        self.assertEquals(len(selected_individuals), len(population))

    def test_when_population_size_is_bigger_than_selection_size(self):
        """ The best individuals are returned. """
        p_size = 10
        selection_size = int(p_size / 2)
        population = utils.DummyPopulation(size=p_size)
        individuals = BestIndividual()(population, selection_size)
        self.assertEquals(len(individuals), selection_size)
        for i in range(len(individuals)):
            self.assertEquals(individuals[i], population[i])


class TournamentTestCase(TestCase):
    """ Tests for BestIndividual selection method. """

    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(Tournament(sample_size=5), f)

    def test_when_population_size_is_lower_than_selection_size(self):
        """ Cannot select more individuals than population size. """
        p_size = 10
        population = utils.DummyPopulation(size=p_size)

        with self.assertRaises(PyneticsError):
            Tournament(sample_size=int(p_size / 2))(population, p_size * 2)

    def test_when_population_size_is_equals_to_selection_size(self):
        """ All the population is returned. """
        p_size = 10
        population = utils.DummyPopulation(size=p_size)
        selected_individuals = Tournament(
            sample_size=int(p_size / 2)
        )(population, p_size)
        self.assertTrue(len(population) >= len(set(selected_individuals)))

    def test_when_population_size_is_bigger_than_selection_size(self):
        """ The best individuals are returned. """
        p_size = 10
        selection_size = int(p_size / 2)
        population = utils.DummyPopulation(size=p_size)
        individuals = Tournament(sample_size=int(p_size / 2))(
            population,
            selection_size
        )
        self.assertEquals(len(individuals), selection_size)
