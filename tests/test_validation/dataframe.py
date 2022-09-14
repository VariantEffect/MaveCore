from unittest import TestCase
import pandas as pd

from mavecore.validation.dataframe import *


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
        dataframe = pd.DataFrame(
            {
                general.hgvs_nt_column: ["c.1A>G"],
                "null": ["c.1A>G"],
                "scores": [1.000],
            }
        )
        with self.assertRaises(ValidationError):
            validate_column_names(dataframe.columns)


class TestValidateVariants(TestCase):
    def test_valid_variants(self):
        dataframe = pd.DataFrame(
            {
                general.hgvs_nt_column: ["c.1A>G", "c.1A>G", "c.1A>G"],
                general.hgvs_pro_column: ["p.Leu5Glu", "p.Leu5Glu", "p.Leu5Glu"],
                general.hgvs_splice_column: ["c.1A>G", "c.1A>G", "c.1A>G"],
            }
        )
        validate_variants(dataframe["hgvs_nt"])

    def test_invalid_variants(self):
        pass


class TestVariantsMatchHgvsColumnNames(TestCase):
    def test_valid(self):
        pass

    def test_mismatched_variants_and_column_names(self):
        pass


class TestHgvsColumnsDefineSameVariants(TestCase):
    def test_valid(self):
        pass


class TestDataframesDefineSameVariants(TestCase):
    def test_valid(self):
        scores = pd.DataFrame(
            {
                general.hgvs_nt_column: ["c.1A>G"],
                general.hgvs_pro_column: ["p.Leu5Glu"],
                general.hgvs_splice_column: ["c.1A>G"],
            }
        )
        counts = pd.DataFrame(
            {
                general.hgvs_nt_column: ["c.1A>G"],
                general.hgvs_pro_column: ["p.Leu5Glu"],
                general.hgvs_splice_column: ["c.1A>G"],
            }
        )
        validate_dataframes_define_same_variants(scores, counts)

    def test_counts_defines_different_nt_variants(self):
        scores = pd.DataFrame(
            {
                general.hgvs_nt_column: ["c.1A>G"],
                general.hgvs_pro_column: [None],
                general.hgvs_splice_column: [None],
            }
        )
        counts = pd.DataFrame(
            {
                general.hgvs_nt_column: ["c.2A>G"],
                general.hgvs_pro_column: [None],
                general.hgvs_splice_column: [None],
            }
        )
        with self.assertRaises(ValidationError):
            validate_dataframes_define_same_variants(scores, counts)

    def test_counts_defines_different_splice_variants(self):
        scores = pd.DataFrame(
            {
                general.hgvs_nt_column: [None],
                general.hgvs_splice_column: ["c.1A>G"],
                general.hgvs_pro_column: [None],
            }
        )
        counts = pd.DataFrame(
            {
                general.hgvs_nt_column: [None],
                general.hgvs_splice_column: ["c.2A>G"],
                general.hgvs_pro_column: [None],
            }
        )
        with self.assertRaises(ValidationError):
            validate_dataframes_define_same_variants(scores, counts)

    def test_counts_defines_different_pro_variants(self):
        scores = pd.DataFrame(
            {
                general.hgvs_nt_column: [None],
                general.hgvs_splice_column: [None],
                general.hgvs_pro_column: ["p.Leu5Glu"],
            }
        )
        counts = pd.DataFrame(
            {
                general.hgvs_nt_column: [None],
                general.hgvs_splice_column: [None],
                general.hgvs_pro_column: ["p.Leu75Glu"],
            }
        )
        with self.assertRaises(ValidationError):
            validate_dataframes_define_same_variants(scores, counts)