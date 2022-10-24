from unittest import TestCase

from mavecore.validation.constants.general import null_values_list
from mavecore.validation.variant import validate_pro_variant, validate_nt_variant

from mavecore.validation.utilities import (
    is_null,
    generate_hgvs,
    construct_hgvs_pro,
    convert_hgvs_nt_to_hgvs_pro,
    _is_wild_type,
    _is_deletion,
    _is_substitution_one_base,
    _is_substitution_two_bases_nonadjacent
)


class TestIsNull(TestCase):
    def test_valid_null_values(self):
        for value in null_values_list:
            self.assertTrue(is_null(value))

    def test_invalid_null_values(self):
        self.assertFalse(is_null(1))
        self.assertFalse(is_null("1"))


class TestGenerateHgvsPro(TestCase):
    def test_pro(self):
        pass

    def test_nt(self):
        pass


class TestConstructHgvsPro(TestCase):
    def valid_arguments(self):
        pass

    def invalid_wt_aa(self):
        pass

    def invalid_mut_aa(self):
        pass

    def invalid_position(self):
        pass


class TestConvertHgvsNtToHgvsPro(TestCase):
    def invalid_hgvs_nt(self):
        pass

    def wt_hgvs_nt(self):
        pass

    def deletion_hgvs_nt(self):
        pass

    def one_base_change_codon_variant(self):
        pass

    def two_base_change_codon_variant(self):
        pass

    def three_base_change_codon_variant(self):
        pass


class TestVariantTypeHelperFunctions(TestCase):

    def test_is_wild_type(self):
        pass

    def is_deletion(self):
        pass

    def test_is_substitution_one_base(self):
        pass

    def test_is_substitution_two_bases_nonadjacent(self):
        pass
