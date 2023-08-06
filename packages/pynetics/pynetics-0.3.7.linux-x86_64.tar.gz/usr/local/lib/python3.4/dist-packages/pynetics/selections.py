import operator
import random

from pynetics import Selection


class BestIndividual(Selection):
    """ Selects the best individuals among the population. """

    def perform(self, population, n):
        """ Gets the top n individuals out of all the population.

        If "repetable" is activated, the returned individuals will be n times
        the best individual. If False, the returned individuals will be the top
        n individuals.

        :param population: The population from which select the individuals.
        :param n: The number of individuals to return.
        :return: A list of n individuals.
        """
        return population[:n]


class ProportionalToPosition(Selection):
    """ Selects individuals randomly proportionally to their position. """

    def perform(self, population, n):
        """ Gets randomly the individuals, giving more probability to those in
        first positions of the population, i.e. those fittest.

        The probability to be selected is proportional to the position of the
        fitness of the individual among the population (i.e. those with better
        fitness have better positions, but a very high fitness doesn't implies
        more chances to be selected).

        If "repetable" is activated, the returned individuals may be repeated.

        :param n: The number of individuals to return.
        :param population: The population from which select the individuals.
        :return: A list of n individuals.
        """
        # TODO Implement
        raise NotImplementedError()


class Tournament(Selection):
    """ Selects best individuals of a random sample of the whole population. """

    def __init__(self, sample_size):
        """ Initializes this selector.

        :param sample_size: The size of the random sample of individuals to pick
            prior to make the selection of the fittest.
        :param repetable: If repetition of individuals is allowed. If true,
            there are chances of the same individual be selected again. Defaults
            to False.
        """
        self.sample_size = sample_size

    def perform(self, population, n):
        """ Gets the best individuals from a random sample of the population.

        To do it, a sample of individuals will be selected randomly and, after
        that, the best individual of the sample is then selected. This process
        (i.e. extract sample and the get best individual from sample) is done
        as many times as individuals to be selected.

        If "rep" is activated, the returned individuals may be repeated.

        :param n: The number of individuals to return.
        :param population: The population from which select the individuals.
        :return: A list of n individuals.
        """
        individuals = []
        for _ in range(n):
            sample = random.sample(population, self.sample_size)
            individuals.append(
                max(sample, key=operator.methodcaller('fitness'))
            )
        return individuals


class Uniform(Selection):
    """ Selects individuals randomly from the population. """

    def perform(self, population, n):
        """ Selects n individuals randomly from the population.

        The selection is done by following a uniform distribution along the
        entire population.

        :param population: The population from which select the individuals.
        :param n: The number of individuals to return.
        :return: A list of n individuals.
        """
        random.sample(population, n)
