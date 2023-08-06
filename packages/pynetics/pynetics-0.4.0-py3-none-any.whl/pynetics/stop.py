from pynetics import StopCondition


class StepsNum(StopCondition):
    """ If the genetic algorithm has made enough iterations. """

    def __init__(self, steps):
        """ Initializes this function with the number of iterations.

        :param steps: The number of iterations to do before stop.
        """
        self.steps = steps

    def __call__(self, genetic_algorithm):
        """ Checks if this stop criteria is met.

        It will look at the generation of the genetic algorithm. It's expected
        that, if its generation is greater or equal than the specified in
        initialization method, the criteria is met.

        :param genetic_algorithm: The genetic algorithm where this stop
            condition belongs.
        :return: True if criteria is met, false otherwise.
        """
        return genetic_algorithm.generation >= self.steps


class FitnessBound(StopCondition):
    """ If the genetic algorithm obtained a fine enough individual. """

    def __init__(self, fitness_bound):
        """ Initializes this function with the upper bound for the fitness.

        :param fitness_bound: A fitness value. The criteria will be met when the
            fitness in the algorithm (in one or all populations managed, see
            below) is greater than this specified fitness.
        """
        self.fitness_bound = fitness_bound

    def __call__(self, genetic_algorithm):
        """ Checks if this stop criteria is met.

        It will look at the fitness of the best individual the genetic algorithm
        has discovered. In case of its fitness being greater or equal than the
        specified at initialization time, the condition will be met and the
        algorithm will stop.

        :param genetic_algorithm: The genetic algorithm where this stop
            condition belongs.
        :return: True if criteria is met, false otherwise.
        """
        return genetic_algorithm.best().fitness() >= self.fitness_bound
