from unittest import TestCase

from pynetics.gggp import grammar


class SingleTermTestCase(TestCase):
    """ Test for SingleTerm instances. """

    def test_value_is_not_a_string(self):
        """ Param "value" should be a string. """
        for invalid_value in ([], (), {}, None, grammar.SingleTerm('hello')):
            with self.assertRaises(ValueError):
                grammar.SingleTerm(invalid_value)

    def test_different_instances_with_same_content_are_equal(self):
        """ If two different instances has the same content are equal. """
        self.assertEquals(
            grammar.SingleTerm('t'),
            grammar.SingleTerm('t'),
        )

    def test_correct_value_as_a_string(self):
        """ If value is a string, the term initializes correctly. """
        string_value = 'terminal'
        self.assertEquals(string_value, grammar.SingleTerm(string_value).value)


class AndTestCase(TestCase):
    """ Test for And connector instances. """

    def test_value_is_not_a_tuple(self):
        """ If value is not a tuple, an error is raised. """
        with self.assertRaises(ValueError):
            grammar.And(grammar.SingleTerm('terminal'))

    def test_value_is_a_tuple_of_less_than_two_terms(self):
        """ If value is a tuple of less than 2 terms, an error is raised. """
        invalid_values = (
            tuple(),
            grammar.SingleTerm('terminal'),
        )
        for value in invalid_values:
            with self.assertRaises(ValueError):
                grammar.And(value)

    def test_not_all_values_in_value_tuple_are_terms_or_strings(self):
        """ If elements in value are not Term, an error is raised. """
        invalid_values = (
            (grammar.SingleTerm('terminal'), 'a nice dog', 9),
            (1, 2, 3, 4, 5),
        )
        for value in invalid_values:
            with self.assertRaises(ValueError):
                grammar.And(value)

    def test_different_instances_with_same_content_are_equal(self):
        """ If two different instances has the same content are equal. """
        value = (
            grammar.SingleTerm('terminal1'),
            'terminal2'
        )
        self.assertEquals(
            grammar.And(*value),
            grammar.And(*value),
        )

    def test_correct_construction(self):
        """ If value is correct, the term is correctly initialized. """
        value = (
            grammar.SingleTerm('terminal1'),
            'terminal2'
        )
        and_connector = grammar.And(*value)
        self.assertEquals(value[0], and_connector.value[0])
        self.assertEquals(grammar.SingleTerm(value[1]), and_connector.value[1])


class OrTestCase(TestCase):
    """ Test for Or connector instances. """

    def test_value_is_not_a_tuple(self):
        """ If value is not a tuple, it raises an error. """
        with self.assertRaises(ValueError):
            grammar.Or(grammar.SingleTerm('terminal'))

    def test_value_is_a_tuple_of_less_than_two_terms(self):
        """ If value is a tuple of less than 2 terms, it raises an error. """
        invalid_values = (
            tuple(),
            grammar.SingleTerm('terminal'),
        )
        for value in invalid_values:
            with self.assertRaises(ValueError):
                grammar.Or(value)

    def test_not_all_values_in_value_tuple_are_not_term_string_or_tuple(self):
        """ If value is a tuple of less than 2 terms, it raises an error. """
        invalid_values = (
            (grammar.SingleTerm('terminal'), 'a nice dog', 9),
            (1, 2, 3, 4, 5),
        )
        for value in invalid_values:
            with self.assertRaises(ValueError):
                grammar.Or(value)

    def test_if_values_in_value_are_tuples_not_all_weights_are_numbers(self):
        """ If value is a tuple of less than 2 terms, it raises an error. """
        with self.assertRaises(ValueError):
            grammar.Or((
                (grammar.SingleTerm('terminal'), 2),
                (grammar.SingleTerm('terminal'), '8'),
            ))

    def test_correct_construction_with_weights(self):
        """ If value correct with weights, term is correctly initialized. """
        value_and_weights = (
            (grammar.SingleTerm('t1'), 1),
            ('t2', 3),
        )
        value = tuple(t[0] for t in value_and_weights)
        weights = tuple(t[1] for t in value_and_weights)

        or_connector = grammar.Or(*value_and_weights)
        self.assertEquals(value[0], or_connector.value[0])
        self.assertEquals(grammar.SingleTerm(value[1]), or_connector.value[1])
        self.assertEquals(weights, or_connector.weights)

    def test_different_instances_with_same_content_are_equal(self):
        """ If two different instances has the same content are equal. """
        value = (
            grammar.SingleTerm('terminal1'),
            'terminal2'
        )
        self.assertEquals(
            grammar.Or(*value),
            grammar.Or(*value),
        )

    def test_correct_construction_without_weights(self):
        """ If value correct without weights, term is correctly initialized. """
        value = (
            grammar.SingleTerm('t1'),
            't2',
        )

        or_connector = grammar.Or(*value)
        self.assertEquals(value[0], or_connector.value[0])
        self.assertEquals(grammar.SingleTerm(value[1]), or_connector.value[1])
        self.assertEquals(tuple(1 for _ in value), or_connector.weights)


class MultiplierTestCase(TestCase):
    """ Test for Multiplier instances. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__default_lower = 0
        self.__default_upper = float('Inf')
        self.__default_p = 0.5

    def test_value_is_not_a_term_or_is_a_multiple_term(self):
        """ Param value should be a term other than Multiplier instance. """
        for invalid_value in (
            [],
            (),
            {},
            None,
            grammar.Multiplier(grammar.SingleTerm('t')),
        ):
            with self.assertRaises(ValueError):
                grammar.Multiplier(invalid_value)

    def test_p_should_be_an_int_or_float(self):
        """ Value p should be a number between 0.0 and 1.0 both incl. """
        for invalid_p in (
            [],
            (),
            {},
            None,
            '7',
            -0.1,
            1.1,
        ):
            with self.assertRaises(ValueError):
                grammar.Multiplier(grammar.SingleTerm('t'), p=invalid_p)

    def test_different_instances_with_same_content_are_equal(self):
        """ If two different instances has the same content are equal. """
        self.assertEquals(
            grammar.Multiplier('t'),
            grammar.Multiplier('t'),
        )

    def test_correct_construction_with_string_without_anything(self):
        """ Correct construction without optional params and a string term.

        That means that "lower", "upper" and "p" take the correct values.
        """
        str_value = 't'
        value = grammar.SingleTerm(str_value)
        multiplier = grammar.Multiplier(str_value)
        self.assertEquals(value, multiplier.value)
        self.assertEquals(self.__default_lower, multiplier.lower)
        self.assertEquals(self.__default_upper, multiplier.upper)
        self.assertAlmostEqual(self.__default_p, multiplier.p)

    def test_correct_construction_with_string_with_only_lower(self):
        """ Correct construction with only "lower" param and a string term.

        That means that "upper" and "p" take the correct values.
        """
        str_value = 't'
        value = grammar.SingleTerm(str_value)
        lower = 1
        multiplier = grammar.Multiplier(str_value, lower=lower)
        self.assertEquals(value, multiplier.value)
        self.assertEquals(lower, multiplier.lower)
        self.assertEquals(self.__default_upper, multiplier.upper)
        self.assertAlmostEqual(self.__default_p, multiplier.p)

    def test_correct_construction_with_string_with_only_upper(self):
        """ Correct construction with only "upper" param and a string term.

        That means that "lower" and "p" take the correct values.
        """
        str_value = 't'
        value = grammar.SingleTerm(str_value)
        upper = 1
        multiplier = grammar.Multiplier(str_value, upper=upper)
        self.assertEquals(value, multiplier.value)
        self.assertEquals(self.__default_lower, multiplier.lower)
        self.assertEquals(upper, multiplier.upper)
        self.assertAlmostEqual(self.__default_p, multiplier.p)

    def test_correct_construction_with_string_with_only_p(self):
        """ Correct construction with only "p" param and a string term.

        That means that "lower" and "upper" take the correct values.
        """
        str_value = 't'
        value = grammar.SingleTerm(str_value)
        p = 0.2
        multiplier = grammar.Multiplier(str_value, p=p)
        self.assertEquals(value, multiplier.value)
        self.assertEquals(self.__default_lower, multiplier.lower)
        self.assertEquals(self.__default_upper, multiplier.upper)
        self.assertAlmostEqual(p, multiplier.p)

    def test_correct_construction_with_string_with_lower_and_upper(self):
        """ Correct construction with only "lower" and "upper" param and a
        string term.

        That means that "p" takes the correct value.
        """
        str_value = 't'
        value = grammar.SingleTerm(str_value)
        lower = 3
        upper = 5
        multiplier = grammar.Multiplier(str_value, lower=lower, upper=upper)
        self.assertEquals(value, multiplier.value)
        self.assertEquals(lower, multiplier.lower)
        self.assertEquals(upper, multiplier.upper)
        self.assertAlmostEqual(self.__default_p, multiplier.p)

    def test_correct_construction_with_string_with_lower_and_p(self):
        """ Correct construction with only "lower" and "p" param and a
        string term.

        That means that "upper" takes the correct value.
        """
        str_value = 't'
        value = grammar.SingleTerm(str_value)
        lower = 7
        p = 0.75
        multiplier = grammar.Multiplier(str_value, lower=lower, p=p)
        self.assertEquals(value, multiplier.value)
        self.assertEquals(lower, multiplier.lower)
        self.assertEquals(self.__default_upper, multiplier.upper)
        self.assertAlmostEqual(p, multiplier.p)

    def test_correct_construction_with_string_with_upper_and_p(self):
        """ Correct construction with only "upper" and "p" param and a
        string term.

        That means that "lower" takes the correct value.
        """
        str_value = 't'
        value = grammar.SingleTerm(str_value)
        upper = 7
        p = 0.75
        multiplier = grammar.Multiplier(str_value, upper=upper, p=p)
        self.assertEquals(value, multiplier.value)
        self.assertEquals(self.__default_lower, multiplier.lower)
        self.assertEquals(upper, multiplier.upper)
        self.assertAlmostEqual(p, multiplier.p)

    def test_correct_construction_with_string_with_lower_upper_and_p(self):
        """ Correct construction with all optional params and a string term. """
        str_value = 't'
        value = grammar.SingleTerm(str_value)
        lower = 1
        upper = 7
        p = 0.75
        multiplier = grammar.Multiplier(
            str_value,
            lower=lower,
            upper=upper,
            p=p
        )
        self.assertEquals(value, multiplier.value)
        self.assertEquals(lower, multiplier.lower)
        self.assertEquals(upper, multiplier.upper)
        self.assertAlmostEqual(p, multiplier.p)

    def test_correct_construction_with_term_without_anything(self):
        """ Correct construction without optional params and a term instance.

        That means that "lower", "upper" and "p" take the correct values.
        """
        value = grammar.SingleTerm('t')
        multiplier = grammar.Multiplier(value)
        self.assertEquals(value, multiplier.value)
        self.assertEquals(self.__default_lower, multiplier.lower)
        self.assertEquals(self.__default_upper, multiplier.upper)
        self.assertAlmostEqual(self.__default_p, multiplier.p)

    def test_correct_construction_with_term_with_only_lower(self):
        """ Correct construction with only "lower" param and a term instance.

        That means that "upper" and "p" take the correct values.
        """
        value = grammar.SingleTerm('t')
        lower = 1
        multiplier = grammar.Multiplier(value, lower=lower)
        self.assertEquals(value, multiplier.value)
        self.assertEquals(lower, multiplier.lower)
        self.assertEquals(self.__default_upper, multiplier.upper)
        self.assertAlmostEqual(self.__default_p, multiplier.p)

    def test_correct_construction_with_term_with_only_upper(self):
        """ Correct construction with only "upper" param and a term instance.

        That means that "lower" and "p" take the correct values.
        """
        value = grammar.SingleTerm('t')
        upper = 1
        multiplier = grammar.Multiplier(value, upper=upper)
        self.assertEquals(value, multiplier.value)
        self.assertEquals(self.__default_lower, multiplier.lower)
        self.assertEquals(upper, multiplier.upper)
        self.assertAlmostEqual(self.__default_p, multiplier.p)

    def test_correct_construction_with_term_with_only_p(self):
        """ Correct construction with only "p" param and a term instance.

        That means that "lower" and "upper" take the correct values.
        """
        value = grammar.SingleTerm('t')
        p = 0.2
        multiplier = grammar.Multiplier(value, p=p)
        self.assertEquals(value, multiplier.value)
        self.assertEquals(self.__default_lower, multiplier.lower)
        self.assertEquals(self.__default_upper, multiplier.upper)
        self.assertAlmostEqual(p, multiplier.p)

    def test_correct_construction_with_term_with_lower_and_upper(self):
        """ Correct construction with only "lower" and "upper" params and a
        term instance.

        That means that "p" takes the correct value.
        """
        value = grammar.SingleTerm('t')
        lower = 3
        upper = 5
        multiplier = grammar.Multiplier(value, lower=lower, upper=upper)
        self.assertEquals(value, multiplier.value)
        self.assertEquals(lower, multiplier.lower)
        self.assertEquals(upper, multiplier.upper)
        self.assertAlmostEqual(self.__default_p, multiplier.p)

    def test_correct_construction_with_term_with_lower_and_p(self):
        """ Correct construction with only "lower" and "p" params and a
        term instance.

        That means that "upper" takes the correct value.
        """
        value = grammar.SingleTerm('t')
        lower = 7
        p = 0.75
        multiplier = grammar.Multiplier(value, lower=lower, p=p)
        self.assertEquals(value, multiplier.value)
        self.assertEquals(lower, multiplier.lower)
        self.assertEquals(self.__default_upper, multiplier.upper)
        self.assertAlmostEqual(p, multiplier.p)

    def test_correct_construction_with_term_with_upper_and_p(self):
        """ Correct construction with only "upper" and "p" params and a
        term instance.

        That means that "lower" takes the correct value.
        """
        value = grammar.SingleTerm('t')
        upper = 7
        p = 0.75
        multiplier = grammar.Multiplier(value, upper=upper, p=p)
        self.assertEquals(value, multiplier.value)
        self.assertEquals(self.__default_lower, multiplier.lower)
        self.assertEquals(upper, multiplier.upper)
        self.assertAlmostEqual(p, multiplier.p)

    def test_correct_construction_with_term_with_lower_upper_and_p(self):
        """ Correct construction with all params and a term instance. """
        value = grammar.SingleTerm('t')
        lower = 1
        upper = 7
        p = 0.75
        multiplier = grammar.Multiplier(value, lower=lower, upper=upper, p=p)
        self.assertEquals(value, multiplier.value)
        self.assertEquals(lower, multiplier.lower)
        self.assertEquals(upper, multiplier.upper)
        self.assertAlmostEqual(p, multiplier.p)


class TestProduction(TestCase):
    """ Tests the production rules work properly. """

    def test_init_fails_if_term_is_not_a_term_instance(self):
        """ Beta should be a list and not a simple object. """
        variable = 'variable'
        for invalid_term in (
            [grammar.EpsilonTerminal, ],
            (grammar.EpsilonTerminal,),
            {'terminal': grammar.EpsilonTerminal},
            None,
            '7',
            42,
        ):
            with self.assertRaises(ValueError):
                grammar.Production(variable, invalid_term)

    def test_correct_construction(self):
        """ Tests alpha is assigned to a read_only property. """
        variable = 'non-terminal'

        production = grammar.Production(variable, grammar.EpsilonTerminal)
        self.assertEquals(variable, production.variable)
        self.assertEquals(grammar.EpsilonTerminal, production.term)


class GrammarTestCase(TestCase):
    """ Tests for Grammar instances. """

    def test_start_symbol_should_exists_as_variable_in_productions(self):
        """ The start symbol must lead at least one of the productions. """
        existent_start_symbol = 'existent'
        non_existent_start_symbol = 'non_existent'

        productions = [
            grammar.Production(
                existent_start_symbol,
                grammar.EpsilonTerminal
            ) for _ in range(4)
            ]

        # Test OK if start_symbol exists.
        grammar.Grammar(
            start_symbol=existent_start_symbol,
            productions=productions
        )
        # Test KO if start_symbol_does_not_exists
        with self.assertRaises(ValueError):
            grammar.Grammar(
                start_symbol=non_existent_start_symbol,
                productions=productions
            )

    def test_productions_should_be_an_list_of_production_instances(self):
        """ Productions should be a list of Production instances. """
        all_but_one = [
            grammar.Production(
                't',
                grammar.EpsilonTerminal
            ) for _ in range(4)
            ]
        all_but_one.append(grammar.EpsilonTerminal)
        for invalid_productions in (
            (),
            {},
            None,
            'terminal',
            ['terminal'],
            grammar.EpsilonTerminal,
            [grammar.EpsilonTerminal],
            all_but_one,
        ):
            with self.assertRaises(ValueError):
                grammar.Grammar('terminal', invalid_productions)

    def test_correct_construction(self):
        """ Correct start_symbol and productions lead to a correct grammar. """
        base_symbol = 't'
        start_symbol = base_symbol + '0'
        productions = [
            grammar.Production(
                base_symbol + str(i),
                grammar.EpsilonTerminal
            ) for i in range(4)
            ]

        a_grammar = grammar.Grammar(
            start_symbol=start_symbol,
            productions=productions
        )
        self.assertEquals(start_symbol, a_grammar.start_symbol)
        for production in productions:
            self.assertIn(production, a_grammar.productions)
        for production in a_grammar.productions:
            self.assertIn(production, productions)

    def test_repeated_productions_are_shrunk(self):
        """ If two or more productions has the same alpha, they're shrunk.

        This implies that if two or more productions has the same alpha, they're
        transformed in a single production with all the beta parts of the
        productions separated by Or's.
        """
        start_symbol = 'expr'
        productions = [
            grammar.Production(
                'expr',
                grammar.SingleTerm(str(i))
            ) for i in range(10)
            ]
        a_grammar = grammar.Grammar(start_symbol, productions)

        # The ten productions are transformed in One
        self.assertEquals(len(a_grammar.productions), 1)
        # The only term of the productions is an Or instance
        production = a_grammar.productions[0]
        self.assertEquals(start_symbol, production.variable)
        self.assertIsInstance(production.term, grammar.Or)
        # The Or term contains all the terms in initial productions.
        value = production.term.value
        for t in value:
            self.assertIn(t, [p.term for p in productions])
        for t in [p.term for p in productions]:
            self.assertIn(t, value)

# TODO Test grammar.variables
# TODO Test grammar.terminals
# TODO Test Term.random_derivation (all of the terms)
# TODO Test DerivationTree
