import random


def take_chances(probability=0.5):
    """ Given a probability, the method generates a random value to see if is
        lower or not than that probability.

    :param probability: The value of the probability to beat. Default is 0.5.
    :return: A value of True if the value geneated is bellow the probability
        specified, and false otherwise.
    """
    return random.random() < probability


def clone_empty(obj):
    """ Used by classes which need to be cloned avoiding the call to __init__.

    :param obj: The object to be cloned.
    :return: A newly empty object of the class obj.
    """

    class Empty(obj.__class__):
        def __init__(self): pass

    empty = Empty()
    empty.__class__ = obj.__class__
    return empty
