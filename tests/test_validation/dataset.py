from unittest import TestCase
from mavecore.validation.exceptions import ValidationError


class TestValidateNoNullColumnsRows(TestCase):
    def test_valid(self):
        pass

    def test_null_row(self):
        pass

    def test_null_column(self):
        pass


class TestValidateColumnNames(TestCase):
    def test_valid_column_names(self):
        pass

    def test_missing_hgvs_column(self):
        pass

    def test_hgvs_in_wrong_location(self):
        pass

    def test_no_additional_columns_beyond_hgvs(self):
        pass

    def test_null_column_name(self):
        pass


class TestValidateVariants(TestCase):
    def test_valid_variants(self):
        pass

    def test_invalid_variants(self):
        pass


class TestVariantsMatchHgvsColumnNames(TestCase):
    def test_valid(self):
        pass

    def test_mismatched_variants_and_column_names(self):
        pass


class TestDataframesDefineSameVariants(TestCase):
    def test_valid(self):
        pass

    def test_dataframes_do_not_define_same_variants(self):
        pass