import decimal
import unittest

import lvars
import mfs
from exceptions import FuzzleError
from lvars import LinguisticVariable


class LinguisticVariableTestCase(unittest.TestCase):
    """ Tests for linguistic variables. """

    def test_wrong_names(self):
        """ The name cannot be other than a non empty string. """
        wrong_names = None, '', 42, 5.5, [1, 2, 3], (1, 2, 3), {1: 2}
        with self.assertRaises(FuzzleError):
            [LinguisticVariable(name, (0, 1)) for name in wrong_names]

    def test_wrong_domains(self):
        """ The domain should be a tuple of numeric values. """
        wrong_domains = None, '', '0, 1', [0, 1], 42,
        with self.assertRaises(FuzzleError):
            [LinguisticVariable('Var', domain) for domain in wrong_domains]

    def test_valid_construction(self):
        """ Check if construction is performed with valid param. values. """
        valid_names = 'Variable 1', 'Variable 2', 'Variable 3',
        valid_domains = (
            (0, 1),
            (7.9, 5.5),
            (decimal.Decimal(0), decimal.Decimal(1)),
        )
        for name in valid_names:
            for domain in valid_domains:
                lvar = LinguisticVariable(name, domain)
                self.assertEquals(name, lvar.name)
                self.assertEquals(
                        tuple(sorted([float(x) for x in domain])),
                        lvar.domain
                )

    def test_wrong_values_to_fuzzify(self):
        """ A non numeric value to fuzzify leads to an error. """
        ivar = lvars.InputLVar('Variable', (-1, 1))
        ivar['fs'] = mfs.TriMF(-1, 0, 1)

        wrong_values = None, '', '0, 1', [0, 1],
        for x in wrong_values:
            with self.assertRaises(FuzzleError):
                ivar.fuzzify(x)
