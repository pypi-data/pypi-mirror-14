import random

from pynetics.ga_list import Alleles, ListRecombination


class RealIntervalAlleles(Alleles):
    """ The possible alleles are real numbers belonging to an interval. """

    def __init__(self, a, b):
        """ Initializes the alleles with the interval of all their valid values

        It doesn't matters the order of the parameters. The interval will be all
        the real numbers between the lower and the upper values.

        :param a: One end of the interval.
        :param b: Other end of the interval.
        """
        self.a = min(a, b)
        self.b = max(a, b)

    def get(self):
        """ A random value is selected uniformly over the interval. """
        return random.uniform(self.a, self.b)


class PlainRecombination(ListRecombination):
    def __call__(self, parent1, parent2):
        """ Realizes the crossover operation.

        :param parent1: One of the individuals from which generate the progeny.
        :param parent2: The other.
        :return: A list of two individuals, each one a child containing some
            characteristics derived from the parents.
        """
        child1, child2 = super().__call__(parent1, parent2)
        for g in range(len(parent1)):
            lower_bound = min(parent1[g], parent2[g])
            upper_bound = max(parent1[g], parent2[g])

            child1[g] = random.uniform(lower_bound, upper_bound)
            child2[g] = upper_bound - (child1[g] - lower_bound)
        return child1, child2


class MorphologicalRecombination(ListRecombination):
    # TODO We need to improve this crossover (maybe a diversity for population?)
    """Crossover that changes its behaviour depending on population diversity.

    The idea is that, for each dimension of the vector (the chromosome of the
    list individual) the algorithm first see how diverse is this dimension in
    the population, that is, how big is the maximum difference between values
    of different individuals in the same dimension. If the difference is to big,
    the algorithm will choose the value of the children from a smaller interval
    whereas if the diversity is to low, the algorithm will increase the interval
    to increase the diversity.

    NOTE: Works only for individuals with list chromosomes of real interval
    alleles.
    NOTE: The value of each gene must be normalized to the interval [0, 1].
    """

    def __init__(self, a=-.001, b=-.133, c=.54, d=.226):
        # TODO TBD Search the reference to the papers .
        """ Initializes this crossover method.

        The parameters a, b, c, d are the stated on paper: [INSERT HERE THE
        REFERENCE]

        :param a: One of the parameters.
        :param b: Other parameter.
        :param c: Yes, other parameter.
        :param d: Ok, the last parameter is this.
        """
        self.__a = a
        self.__b = b
        self.__c = c
        self.__d = d

        self.__calc_1 = (b - a) / c
        self.__calc_2 = d / (1 - c)
        self.__calc_3 = self.__calc_2 * -c

    def __call__(self, parent1, parent2):
        """ Realizes the crossover operation.

        :param parent1: One of the individuals from which generate the progeny.
        :param parent2: The other.
        :return: A list of two individuals, each one a child containing some
            characteristics derived from the parents.
        """
        child1, child2 = super().__call__(parent1, parent2)
        for g in range(len(parent1)):
            genes_in_position_g = [i[g] for i in parent1.population]
            diversity = max(genes_in_position_g) - min(genes_in_position_g)

            phi = self.__phi(diversity)
            lower_bound = min(parent1[g], parent2[g]) + phi
            upper_bound = max(parent1[g], parent2[g]) - phi

            child1[g] = random.uniform(lower_bound, upper_bound)
            child2[g] = upper_bound - (child1[g] - lower_bound)
        return child1, child2

    def __phi(self, x):
        """ Value in the interval from where to obtain the values grow or shrink

        :param x: The value of the diversity
        :return:
        """
        if x <= self.__c:
            return self.__calc_1 * x + self.__a
        else:
            return self.__calc_2 * x + self.__calc_3
