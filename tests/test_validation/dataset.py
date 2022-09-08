from unittest import TestCase
import pandas as pd

from mavecore.validation.constants import general
from mavecore.validation.exceptions import ValidationError
from mavecore.validation.dataset import *


class TestValidateNoNullColumnsOrRows(TestCase):
    def test_valid(self):
        dataframe = pd.DataFrame(
            {
                general.hgvs_nt_column: ["c.1A>G"],
                general.hgvs_pro_column: ["p.Leu5Glu"],
                general.hgvs_splice_column: ["c.1A>G"],
            }
        )
        validate_no_null_columns_or_rows(dataframe)

    def test_null_row(self):
        dataframe = pd.DataFrame(
            {
                general.hgvs_nt_column: ["c.1A>G", None],
                general.hgvs_pro_column: ["p.Leu5Glu", None],
                general.hgvs_splice_column: ["c.1A>G", None],
            }
        )
        with self.assertRaises(AssertionError):
            validate_no_null_columns_or_rows(dataframe)

    def test_null_column(self):
        dataframe = pd.DataFrame(
            {
                general.hgvs_nt_column: ["c.1A>G", None],
                general.hgvs_pro_column: [None, None],
                general.hgvs_splice_column: ["c.1A>G", None],
            }
        )
        with self.assertRaises(AssertionError):
            validate_no_null_columns_or_rows(dataframe)


class TestValidateColumnNames(TestCase):
    def test_valid_column_names(self):
        dataframe = pd.DataFrame(
            {
                general.hgvs_nt_column: ["c.1A>G"],
                general.hgvs_pro_column: ["p.Leu5Glu"],
                general.hgvs_splice_column: ["c.1A>G"],
                "scores": [1.000],
            }
        )
        validate_column_names(dataframe.columns)

    def test_missing_hgvs_column(self):
        dataframe = pd.DataFrame(
            {
                "scores": [1.000],
            }
        )
        with self.assertRaises(ValidationError):
            validate_column_names(dataframe.columns)

    def test_hgvs_in_wrong_location(self):
        dataframe = pd.DataFrame(
            {
                general.hgvs_nt_column: ["c.1A>G"],
                "scores": [1.000],
                general.hgvs_splice_column: ["c.1A>G"],
            }
        )
        with self.assertRaises(ValidationError):
            validate_column_names(dataframe.columns)

    def test_no_additional_columns_beyond_hgvs(self):
        dataframe = pd.DataFrame(
            {
                general.hgvs_nt_column: ["c.1A>G"],
            }
        )
        with self.assertRaises(ValidationError):
            validate_column_names(dataframe.columns)

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