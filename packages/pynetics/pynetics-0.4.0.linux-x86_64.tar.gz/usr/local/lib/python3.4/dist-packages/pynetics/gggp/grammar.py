import abc
import collections
import operator
import random

from pynetics import take_chances


class Term(metaclass=abc.ABCMeta):
    """ Any of the elements in the right part of a production.

    A term is an element that represents terminals, non-terminals, connectors,
    multipliers or any combination of them.
    """

    def __init__(self, value):
        """ Initializes the term with a value.

        :param value: The value for this term. Is expected that subclasses
            implements the required validations for this value as Term will only
            maintain its value.
        """
        self.__value = value

    @property
    def value(self):
        """ Returns the value of this term. """
        return self.__value

    @abc.abstractmethod
    def random_derivation(self):
        """ Generates a random derivation of this term.

        The method should give the immediate terms managed under this term. In
        case of terms like SingleTerm or And, the underneath terms are imposed,
        but in case of terms like Or or OneOrMany, the method will return a
        random list of elements (based on the weights, probabilities or
        whatever the term is using).

        Don't make any recursive call in implementations. Return the immediate
        terms; the method "random_tree" of Grammar class will take care of
        generating the tree.

        :return: A tuple of the immediate terms (or strings) managed under this
            term.
        """


class Connector(Term, metaclass=abc.ABCMeta):
    """ A Connector instance holds many elements.

    This elements should be instances of Term class and the order will be
    maintained.
    """

    def __init__(self, *args):
        """ Initializes this instance with the values.

        :param args: All the terms to be considered in this connector. It
            should contain at least 2 terms and all the elements should be
            instances of Term class.
        :raises ValueError: If the value is not a tuple with strings, instances
            of Term or both.
        """
        super().__init__(value=self.__process_args(args))

    @staticmethod
    def __process_args(args):
        """ Checks that value is an instance of string or Term. """
        error_msg = None
        if not isinstance(args, tuple):
            error_msg = 'should be an instance of tuple'
        elif len(args) <= 1:
            error_msg = 'should have at least 2 elements'
        elif not all([isinstance(term, (Term, str)) for term in args]):
            error_msg = 'elements should be Term or string instances'

        if error_msg:
            raise ValueError('Parameter "args" ' + error_msg)
        else:
            return tuple(
                SingleTerm(t) if isinstance(t, str) else t
                for t in args
            )

    def __eq__(self, other):
        """ Tell if this instance is equal to other by its content. """
        if self is other:
            return True
        elif not isinstance(other, Term) or len(self.value) != len(other.value):
            return False
        else:
            return all([t1 == t2 for t1, t2 in zip(self.value, other.value)])


class And(Connector):
    """ This connector represents an And connector.

    This connector holds a tuple of terms that should appear in the stated
    order.
    """

    def random_derivation(self):
        """ This term returns all the managed terms. """
        return self.value


class Or(Connector):
    """ This connector represents an Or connector.

    It holds a tuple of terms from which to choose one. At initialization time
    a list of tuples may be specified instead a list of terms. In that case,
    each tuple should be expressed in the form (t, w) where t is the tuple and w
    the relative weight of that tuple over other. For example, if the input
    terms is as follows:

    term = Or((t_1, 2), (t_2, 1))

    Then t_1 has double chances to be selected over t_2.
    """

    def __init__(self, *args):
        """ Initializes the instance.

        :param value: A list of terms or a list of tuples in the form (t, w)
            where t is the term and w the relative weight of the term over the
            others in the list.
        """
        value, weights = self.__process_value(args)
        super().__init__(*value)
        self.__weights = self.__validate_weights(weights)

    @staticmethod
    def __process_value(value):
        """ Checks value is a tuple of tuples and processes it.

        If it's a tuple but not a tuple of tuples, it will transform it to a
        tuple of tuples where the second term of each nested tuple is a 1.

        :return: A tuple of two tuples, one of the terms and the other with
            their associated weights.
        """
        if not isinstance(value, tuple):
            raise ValueError("Parameter value should be a tuple")
        else:
            possible_tuples = [isinstance(t, tuple) for t in value]
            if any(possible_tuples) and not all(possible_tuples):
                msg = 'Parameter value should be terms or tuples but not both'
                raise ValueError(msg)
            elif not all(possible_tuples):
                return value, tuple(1 for _ in value)
            else:
                return (
                    tuple(t for t, _ in value),
                    tuple(w for _, w in value),
                )

    @staticmethod
    def __validate_weights(weights):
        """ Checks the weights are all int or float instances. """
        if not all([isinstance(w, (int, float)) for w in weights]):
            raise ValueError("Parameter value contains invalid weights")
        else:
            return weights

    @property
    def weights(self):
        """ Returns the weights for the values managed under this term. """
        return self.__weights

    def __eq__(self, o):
        """ Tell if this instance is equal to other by its content. """
        if super().__eq__(o):
            return all([w1 == w2 for w1, w2 in zip(self.weights, o.weights)])
        else:
            return False

    def random_derivation(self):
        """ This term returns a tuple with one of its managed terms.

        The odds for a term to be chosen will be affected by its weight.
        """
        total_w = float(sum(self.weights))
        terms_with_prob = sorted(
            [
                (t, w / total_w) for t, w in
                zip(self.value, self.weights)
                ], key=operator.itemgetter(1)
        )

        selected_p = random.random()
        p = 0
        for element in terms_with_prob:
            p = p + element[1]
            if selected_p <= p:
                return element[0],
        return terms_with_prob[-1],


class Multiplier(Term, metaclass=abc.ABCMeta):
    """ A Multiplier instance that holds a term that may appear many times. """

    def __init__(self, value, *, lower=None, upper=None, p=0.5):
        """ Initializes this instance with the value.

        :param value: The term to be managed. It should be a Term instance other
            than a Multiplier instance.
        :param lower: The minimum times the term should appear according to the
            grammar. It defaults to 0.
        :param upper: The maximum times the term may appear. It defaults to
            infinite, meaning that there is no limit of the times the term may
            appear.
        :param p: In case of generating terms, this param says w
        :raises ValueError: If the value is not a Term instance.
        """
        super().__init__(value=self.__process_value(value))
        self.__lower, self.__upper = self.__process_limits(lower, upper)
        self.__p = self.__check_probability(p)

    @staticmethod
    def __process_value(value):
        """ Processes that the value, validating it.

        For this purpose it will check if value is an instance of Term (other
        than a NToM term) or a string. If it's the former, it will return it. If
        it's the latter, it will return a SingleTerm with the string as it's
        content. If it's not a Term or a string, or if it's a Multiplier, the
        method will raise a ValueError.
        """
        error_msg = None
        if not isinstance(value, (Term, str)):
            error_msg = 'should be an Term instance (but not a Multiplier one)'
        elif isinstance(value, Multiplier):
            error_msg = 'cannot be a NToM instance'

        if error_msg:
            raise ValueError('Parameter "value" ' + error_msg)
        else:
            return SingleTerm(value) if isinstance(value, str) else value

    @staticmethod
    def __process_limits(lower, upper):
        """ Ensure that limits are specified correctly.

        :param lower: The lower bound of the interval.
        :param upper: The upper bound of the interval.
        :return: The correct lower and upper bounds.
        :raises ValueError: If any of the bounds isn't correct (e.g. not an
            integer) or if the upper bound is not greater than the lower bound.
        """
        try:
            lower = int(lower) if lower is not None else 0
            upper = int(upper) if upper is not None else float('Inf')

            if lower < upper:
                return lower, upper
            else:
                ValueError('Upper limit should be greater than lower limit')
        except ValueError:
            raise ValueError('Lower or upper is not an integer')

    @staticmethod
    def __check_probability(p):
        """ Checks p is valid, i.e. a float value x ∈ [0.0, 1.0]. """
        if p is None or not isinstance(p, float) or not (0. <= p <= 1.):
            error_msg = 'The term p should be an float x ∈ [0.0, 1.0]'
            raise ValueError(error_msg)
        else:
            return p

    def __eq__(self, other):
        """ Tell if this instance is equal to other by its content. """
        if self is other:
            return True
        else:
            eq_limits = self.lower == other.lower and self.upper == other.upper
            eq_p = self.p == other.p
            eq_value = self.value == other.value
            return isinstance(other, Term) and eq_limits and eq_p and eq_value

    @property
    def lower(self):
        """ Returns the minimum times a the managed term should appear. """
        return self.__lower

    @property
    def upper(self):
        """ Returns the maximum times this term may appear. """
        return self.__upper

    @property
    def p(self):
        """ Returns the probability of a new appearance of this term. """
        return self.__p

    def random_derivation(self):
        """ Returns a tuple with the managed term according to limits and p.

        The minimum size of the returned tuple will be the lower limit
        specified in the init param "lower". After that, and with a maximum
        of "upper" terms, a new param will be added as long as random tests fall
        under the probability specified.
        """
        terms = [self.value for _ in range(self.lower)]
        while len(terms) < self.upper and take_chances(self.p):
            terms.append(self.value)
        return tuple(terms)


class SingleTerm(Term):
    """ A single term can hold one and only one element.

    This element must be a string (i.e. a variable name or a terminal).
    """

    def __init__(self, value):
        """ Initializes this term with the given value .

        :param value: The value of the term. It should be an string instance.
        :raises ValueError: If the value is not an string.
        """
        super().__init__(value=self.__check_value(value))

    @staticmethod
    def __check_value(value):
        """ Checks that value is an instance of string. """
        if value is None or not isinstance(value, str):
            error_msg = 'The term value should be an instance of string'
            raise ValueError(error_msg)
        else:
            return value

    def __eq__(self, other):
        """ Tell if this instance is equal to other by it's content. """
        if self is other:
            return True
        elif not isinstance(other, Term):
            return False
        else:
            return self.value == other.value

    def random_derivation(self):
        """ Returns a tuple with a number of terms between zero and n. """
        return self.value,


EpsilonTerminal = SingleTerm('ε')


class Production:
    """ A production of the grammar.

    A production rule is a pair of elements (v, t) where v is a grammar variable
    (an element which "produces" or "is replaced by" something) and t is a term
    of terminal and non-terminal elements (that something. See Term for more
    information).
    """

    def __init__(self, variable, term):
        """ Initializes the production rule with its information.

        :param variable: The variable that produces or is replaced by terms.
        :param term: The term of the production. Should be any of the instances
            of Term, otherwise it will raise an error.
        :raises ValueError: If term is not a Term instance.
        """
        self.__variable = variable
        self.__term = self.__validate_term(term)

    @staticmethod
    def __validate_term(term):
        """ Checks and returns the term if there is no error.

        If term is invalid, a ValueError with the error message will be raised.
        """
        if not isinstance(term, Term):
            raise ValueError('Parameter "term" should be a Term instance')
        else:
            return term

    @property
    def variable(self):
        """ Returns the alpha part of this production rule. """
        return self.__variable

    @property
    def term(self):
        """ Returns the beta part of this production rule. """
        return self.__term

    def __eq__(self, other):
        if not self.variable == other.variable:
            return False
        else:
            return self.term == other.term


class Node:
    def __init__(self, value, parent, processed=False):
        self.__value = value
        self.__parent = parent
        self.__processed = processed

    @property
    def value(self):
        return self.__value

    @property
    def parent(self):
        return self.__parent

    @property
    def processed(self):
        return self.__processed

    @processed.setter
    def processed(self, processed):
        self.__processed = processed

    def __str__(self):
        return self.value


class Grammar:
    """ An object which represents a context free grammar. """

    def __init__(self, start_symbol=None, productions=None):
        """ Initializes the grammar.

        :param start_symbol: The start symbol of this grammar. Should exist in
            the productions as a variable. Otherwise it will raise an error.
        :param productions: The list of productions which defines this grammar.
            It should be defined as a list of production instances, otherwise it
            will raise an error. If there are different productions with the
            same variable, they will be shrunk to one single production with an
            Or term connector with their terms.
        :raises ValueError: If "start_symbol" parameter is not present or if it
            exists, it's not empty and does not exists in any of the production
            rules.
        :raises ValueError: If "production_rules" parameter is not present or if
            it is present but is not a valid list of production rules.
        """
        self.__productions = self.__process_productions(productions)
        self.__start_symbol = self.__process_start_symbol(
            start_symbol,
            productions,
        )
        self.__variables = None
        self.__terminals = None

    @staticmethod
    def __process_productions(productions):
        """ Validates the productions raising an error if it's wrong. """
        error_msg = None
        if not productions or not isinstance(productions, list):
            error_msg = 'should be a valid list'
        elif not all([isinstance(p, Production) for p in productions]):
            error_msg = 'contains at least one non-Production instance'
        if error_msg:
            raise ValueError('Parameter "production_rules" ' + error_msg)

        # Everything is ok at this point, so let's shrink the productions
        all_prods = collections.defaultdict(list)
        for production in productions:
            all_prods[production.variable].append(production.term)
        new_productions = []
        for variable, terms in all_prods.items():
            new_productions.append(Production(
                variable=variable,
                term=Or(*terms) if len(terms) > 1 else terms[0],
            ))
        return new_productions

    @staticmethod
    def __process_start_symbol(start_symbol, productions):
        """ Validates the start symbol raising an error if it's wrong. """
        if start_symbol not in [p.variable for p in productions]:
            raise ValueError('Parameter "start_symbol" not in productions')
        else:
            return start_symbol

    @property
    def start_symbol(self):
        """ Returns the start symbol of this grammar. """
        return self.__start_symbol

    @property
    def productions(self):
        """ Returns the production rules for this grammar. """
        return self.__productions

    @property
    def variables(self):
        """ Returns the variables for this grammar. """
        if self.__variables is None:
            self.__variables = set(p.variable for p in self.productions)
        return self.__variables

    @property
    def terminals(self):
        """ Returns the terminals for this grammar. """
        if self.__terminals is None:
            productions = {p.variable: p.term for p in self.productions}
            elements = [self.start_symbol]
            self.__terminals = set()
            while elements:
                element = elements.pop()
                if isinstance(element, (SingleTerm, Multiplier)):
                    elements.append(element.value)
                elif isinstance(element, Connector):
                    elements.extend(element.value)
                elif element in self.variables:
                    elements.append(productions[element])
                else:
                    self.__terminals.add(element)

        return self.__terminals

    def random_tree(self, initial_symbol=None):
        """ Creates a random tree using the specified initial symbol.

        :param initial_symbol: The start symbol from which to generate the tree.
        """
        # I've made this iterative alg. because the recursive one failed a lot
        productions = {p.variable: p.term for p in self.productions}
        root = initial_symbol or self.__start_symbol
        tree = DerivationTree(self, [Node(value=root, parent=None, )])
        i = 0
        while i < len(tree):
            node = tree[i]
            if node.processed:
                i += 1
            else:
                node.processed = True
                if isinstance(node.value, Term):
                    elements = [
                        Node(value=element, parent=node.parent)
                        for element in node.value.random_derivation()
                        ]
                elif node.value in self.variables:
                    elements = [
                        node,
                        Node(
                            value=productions[node.value],
                            parent=i,
                        )
                    ]
                else:
                    # node.value in self.terminals
                    elements = [node]

                tree[i:i + 1] = elements
                i = 0
        return tree


class DerivationTree(list):
    def __init__(self, grammar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__grammar = grammar
        self.__word = None

    def word(self):
        if self.__word is None:
            word = [self[0]]
            i = 0
            while i < len(word):
                node = word[i]
                if node.value in self.grammar.terminals:
                    i += 1
                else:
                    children = [
                        n for n in self
                        if n.parent == self.index(node)
                        ]
                    word[i:i + 1] = children
                    i = 0
            self.__word = tuple(n.value for n in word)
        return self.__word

    @property
    def grammar(self):
        return self.__grammar
