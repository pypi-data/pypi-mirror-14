import pickle
from unittest import TestCase

from tempfile import TemporaryFile

from pynetics import PyneticsError
from pynetics.ga_list import FiniteSetAlleles, ListIndividualSpawningPool, \
    ListIndividual, ListRecombination, OnePointRecombination, \
    TwoPointRecombination, RandomMaskRecombination, SwapGenes, \
    SingleGeneRandomValue
from test import utils


class AllelesTestCase(TestCase):
    """ Tests for instances of the base class Alleles. """

    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(utils.DummyAlleles(), f)


class FiniteSetAllelesTestCase(TestCase):
    """ Tests for instances of the class FiniteSetAlleles. """

    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(FiniteSetAlleles((1, 2, 3)), f)

    def test_sequence_is_maintained_in_class(self):
        """ Checks the sequence is maintained after initializing the object. """
        sequence = [1, 2, 3, 4, 5]
        alleles = FiniteSetAlleles(sequence)
        self.assertListEqual(list(alleles.symbols), sequence)
        self.assertIsNot(alleles.symbols, sequence)
        sequence.append(6)
        self.assertNotEqual(len(alleles.symbols), len(sequence))

    def test_returned_values_belongs_to_the_sequence(self):
        """ Returned symbols cannot be other than the ones in the sequence. """
        sequence = [1, 2, 3]
        alleles = FiniteSetAlleles(sequence)
        for i in range(1000):
            self.assertIn(alleles.get(), sequence)

    def test_alleles_maintains_a_list_of_no_duplicated_values(self):
        """ The values in the maintained without duplicated values. """
        values = 'ACTGACTGTGCA'
        alleles = FiniteSetAlleles(values)

        # Are there any duplicated values?
        self.assertEquals(len(alleles.symbols), len(set(alleles.symbols)))
        # Are the values in the alleles contained in the initialization list?
        [self.assertIn(a, alleles.symbols) for a in values]
        # Are the values in the initialization list contained in the alleles?
        [self.assertIn(a, values) for a in alleles.symbols]


class ListIndividualSpawningPoolTestCase(TestCase):
    """ Tests for the spawning pool that creates ListIndividual instances. """

    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(ListIndividualSpawningPool(
                10,
                utils.DummyAlleles(),
                utils.DummyFitness()
            ), f)

    def test_size_is_correctly_stored_after_initialization(self):
        for size in (10, 100, 1000, 10000, 100000, 1000000):
            spawning_pool = ListIndividualSpawningPool(
                size,
                utils.DummyAlleles(),
                utils.DummyFitness()
            )
            self.assertEquals(size, spawning_pool.size)

    def test_alleles_correctly_stored_after_initialization(self):
        alleles = utils.DummyAlleles()
        spawning_pool = ListIndividualSpawningPool(
            10,
            alleles,
            utils.DummyFitness()
        )
        self.assertEquals(alleles, spawning_pool.alleles)
        self.assertIs(alleles, spawning_pool.alleles)

    def test_created_individuals_are_list_individuals_with_correct_size(self):
        symbols = (0, 1)
        alleles = FiniteSetAlleles(symbols)
        for size in (10, 100, 1000):
            spawning_pool = ListIndividualSpawningPool(
                size,
                alleles,
                utils.DummyFitness()
            )
            for _ in range(10):
                individual = spawning_pool.create()
                self.assertEquals(size, len(individual))
                for g in individual:
                    self.assertIn(g, symbols)


# Maybe instead inherit from list is better inherit from mutablesequence
class ListIndividualTestCase(TestCase):
    """ An individual whose representation is a list of finite values. """

    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(ListIndividual(), f)

    def test_two_individuals_are_different_when_have_different_lengths(self):
        i1 = ListIndividual()
        [i1.append(i) for i in range(10)]
        i2 = ListIndividual()
        [i2.append(i) for i in range(100)]
        self.assertNotEqual(i1, i2)

    def test_two_individuals_are_different_when_have_different_genes(self):
        size = 10
        i1 = ListIndividual()
        [i1.append(1) for _ in range(size)]
        i2 = ListIndividual()
        [i2.append(2) for _ in range(size)]
        self.assertNotEqual(i1, i2)

    def test_two_individuals_are_equal_with_same_lengths_and_genes(self):
        size = 10
        i1 = ListIndividual()
        [i1.append(i) for i in range(size)]
        i2 = ListIndividual()
        [i2.append(i) for i in range(size)]
        self.assertEqual(i1, i2)

    def test_a_cloned_list_individual_is_different_object_but_equal(self):
        i1 = ListIndividual()
        i2 = i1.clone()
        self.assertEquals(i1, i2)
        self.assertIsNot(i1, i2)


class FixedLengthListRecombinationTestCase(TestCase):
    """ Behavior for recombinations where lengths should be the same. """

    class ListRecombinationNoAbstract(ListRecombination):
        def __call__(self, *args, **kwargs):
            return super().__call__(*args, **kwargs)

    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(
                self.ListRecombinationNoAbstract(),
                f
            )

    def test_error_raised_when_parents_of_different_lengths(self):
        symbols = (0, 1)
        alleles = FiniteSetAlleles(symbols)
        sp1 = ListIndividualSpawningPool(10, alleles, utils.DummyFitness())
        sp2 = ListIndividualSpawningPool(100, alleles, utils.DummyFitness())
        parents_list = (
            (sp1.create(), sp2.create()),
            (sp1.create(), sp1.create(), sp2.create()),
            (sp1.create(), sp2.create(), sp2.create()),
            (sp1.create(), sp2.create(), sp1.create()),
            (sp2.create(), sp1.create(), sp2.create()),
        )
        recombination = self.ListRecombinationNoAbstract()
        for parents in parents_list:
            with self.assertRaises(PyneticsError):
                recombination(*parents)

    def test_correct_recombination_of_individuals_with_same_length(self):
        symbols = (0, 1)
        alleles = FiniteSetAlleles(symbols)
        sp = ListIndividualSpawningPool(10, alleles, utils.DummyFitness())
        parents_list = (
            (sp.create(), sp.create()),
            (sp.create(), sp.create(), sp.create()),
            (sp.create(), sp.create(), sp.create(), sp.create()),
        )
        recombination = self.ListRecombinationNoAbstract()
        for parents in parents_list:
            progeny = recombination(*parents)
            self.assertEquals(len(progeny), len(parents))
            for parent, child in zip(parents, progeny):
                self.assertEquals(parent, child)
                self.assertIsNot(parent, child)


class OnePointRecombinationTestCase(TestCase):
    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(OnePointRecombination(), f)

    def test_crossover_is_performed(self):
        """ Checks that one point crossover works as expected. """
        # TODO Not in the mood. Please future me, rewrite it later
        size = 10
        symbols = (0, 1)
        alleles = FiniteSetAlleles(symbols)
        sp = ListIndividualSpawningPool(size, alleles, utils.DummyFitness())
        parents = sp.create(), sp.create()
        progeny = OnePointRecombination()(*parents)

        self.assertEquals(len(progeny), len(parents))
        self.assertEquals(len(parents[0]), len(progeny[0]))
        self.assertEquals(len(parents[1]), len(progeny[1]))


class TwoPointRecombinationTestCase(TestCase):
    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(TwoPointRecombination(), f)

    def test_crossover_is_performed(self):
        """ Checks that one point crossover works as expected. """
        # TODO Not in the mood. Please future me, rewrite it later
        size = 10
        symbols = (0, 1)
        alleles = FiniteSetAlleles(symbols)
        sp = ListIndividualSpawningPool(size, alleles, utils.DummyFitness())
        parents = sp.create(), sp.create()
        progeny = TwoPointRecombination()(*parents)

        self.assertEquals(len(progeny), len(parents))
        self.assertEquals(len(parents[0]), len(progeny[0]))
        self.assertEquals(len(parents[1]), len(progeny[1]))


class RandomMaskRecombinationTestCase(TestCase):
    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(RandomMaskRecombination(), f)

    def test_crossover_is_performed(self):
        """ Checks that one point crossover works as expected. """
        # TODO Not in the mood. Please future me, rewrite it later
        size = 10
        symbols = (0, 1)
        alleles = FiniteSetAlleles(symbols)
        sp = ListIndividualSpawningPool(size, alleles, utils.DummyFitness())
        parents = sp.create(), sp.create()
        progeny = RandomMaskRecombination()(*parents)

        self.assertEquals(len(progeny), len(parents))
        self.assertEquals(len(parents[0]), len(progeny[0]))
        self.assertEquals(len(parents[1]), len(progeny[1]))


class SwapGenesTestCase(TestCase):
    """ Mutates the by swapping two random genes.

    This mutation method operates only with ListIndividuals (or any of their
    subclasses.
    """

    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(SwapGenes(), f)

    def test_check_genes_are_swapped(self):
        """ Checks that the genes of the individual are swapped.

        For this purpose, two checks are performed. First, the method checks if
        there are the same genes in the mutated individual. Second, it checks
        that only two genes has been moved from their positions.
        """
        genes = '0123456789'
        individual = ListIndividual()
        individual.extend(genes)

        mutated = SwapGenes()(individual, p=1)
        # Are all the genes in the individual?
        [self.assertIn(i, mutated) for i in genes]
        # Are only two misplaced genes?
        different_genes = [i for i, j in zip(mutated, individual) if i != j]
        self.assertEquals(len(different_genes), 2)


class RandomGeneValueTestCase(TestCase):
    """ Mutates the individual by changing the value to a random gene. """

    def test_class_is_pickeable(self):
        """ Checks if it's pickeable by writing it into a temporary file. """
        with TemporaryFile() as f:
            pickle.dump(SingleGeneRandomValue(alleles=utils.DummyAlleles()), f)

    def test_check_genes_are_modified(self):
        """ Checks that the genes of the individual are modified.

        For this purpose, two checks are performed. First, the method checks if
        all except one gene are the same. Second, it checks that the different
        gene belongs to the list of allowed values.
        """
        symbols = (0, 1)
        alleles = FiniteSetAlleles(symbols)
        sp = ListIndividualSpawningPool(10, alleles, utils.DummyFitness())
        for _ in range(10):
            individual = sp.create()
            mutated = SingleGeneRandomValue(alleles=alleles)(individual, p=1)
            # Have all the genes values allowed by the alleles?
            self.assertEquals(
                [],
                [i for i in mutated if i not in alleles.symbols]
            )
            # Are all the genes (except one) in the same position?
            different_genes = [i for i, j in zip(mutated, individual) if i != j]
            self.assertEquals(len(different_genes), 1)

    def test_alleles_are_correctly_stored_after_initialization(self):
        symbols = (0, 1)
        alleles = FiniteSetAlleles(symbols)
        mutation = SingleGeneRandomValue(alleles=alleles)

        self.assertEquals(alleles, mutation.alleles)
        self.assertIs(alleles, mutation.alleles)
