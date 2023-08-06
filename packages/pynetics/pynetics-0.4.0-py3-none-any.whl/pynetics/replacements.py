from pynetics import Replacement


class LowElitism(Replacement):
    """ Low elitism replacement.

    The method will replace the less fit individuals by the ones specified in
    the offspring. This makes this operator elitist, but at least not much.
    Moreover, if offspring size equals to the population size then it's a full
    replacement (i.e. a generational scheme).
    """

    def __call__(self, population, individuals):
        """ Removes less fit individuals and then inserts the offspring.

        :param population: The population where make the replacement.
        :param individuals: The new population to use as replacement.
        """
        if individuals:
            population.sort()
            del population[-len(individuals):]
            population.extend(individuals)


class HighElitism(Replacement):
    """ Drops the less fit individuals among all (population plus offspring).

    The method will add all the individuals in the offspring to the population,
    removing afterwards those individuals less fit. This makes this operator
    highly elitist but if length os population and offspring are the same, the
    process will result in a full replacement, i.e. a generational scheme of
    replacement.
    """

    def __call__(self, population, indviduals):
        """ Inserts the offspring in the population and removes the less fit.

        :param population: The population where make the replacement.
        :param indviduals: The new population to use as replacement.
        """
        if indviduals:
            population.sort()
            population.extend(indviduals)
            del population[-len(indviduals):]
