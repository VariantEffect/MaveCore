from unittest import TestCase

from mavecore.validation.constants.general import null_values_list
from mavecore.validation.variant import validate_hgvs_string #validate_pro_variant, validate_nt_variant

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
        pro = generate_hgvs("p")
        validate_hgvs_string(pro)

    def test_nt(self):
        nt = generate_hgvs()
        validate_hgvs_string(nt)


class TestConstructHgvsPro(TestCase):
    def test_valid_arguments(self):
        construct_hgvs_pro(wt="Ala", mutant="Gly", position=3)

    def test_invalid_wt_aa(self):
        with self.assertRaises(ValueError):
            construct_hgvs_pro(wt="Alr", mutant="Gly", position=3)

    def test_invalid_mut_aa(self):
        with self.assertRaises(ValueError):
            construct_hgvs_pro(wt="Ala", mutant="Gla", position=3)

    def test_invalid_position(self):
        # TODO what are the invalid positions we should consider?
        self.assertFalse(False)


class TestConvertHgvsNtToHgvsPro(TestCase):
    def test_invalid_hgvs_nt(self):
        pass

    def test_wt_hgvs_nt(self):
        pass

    def test_deletion_hgvs_nt(self):
        pass

    def test_one_base_change_codon_variant(self):
        pass

    def test_two_base_change_codon_variant(self):
        pass

    def test_three_base_change_codon_variant(self):
        pass


class TestVariantTypeHelperFunctions(TestCase):

    def test_test_is_wild_type(self):
        pass

    def test_is_deletion(self):
        pass

    def test_test_is_substitution_one_base(self):
        pass

    def test_test_is_substitution_two_bases_nonadjacent(self):
        pass
