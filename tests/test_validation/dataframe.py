from unittest import TestCase
import pandas as pd

from mavecore.validation.dataframe import *


class TestValidateNoNullColumnsOrRows(TestCase):
    def setUp(self):
        self.dataframe = pd.DataFrame(
            {
                hgvs_nt_column: ["c.1A>G"],
                hgvs_pro_column: ["p.Leu5Glu"],
                hgvs_splice_column: ["c.1A>G"],
            }
        )

    def test_valid(self):
        validate_no_null_columns_or_rows(self.dataframe)

    def test_null_row(self):
        self.dataframe.loc[1] = [None, None, None]
        with self.assertRaises(AssertionError):
            validate_no_null_columns_or_rows(self.dataframe)

    def test_null_column(self):
        self.dataframe[hgvs_pro_column][0] = None
        with self.assertRaises(AssertionError):
            validate_no_null_columns_or_rows(self.dataframe)


class TestValidateColumnNames(TestCase):
    def setUp(self):
        self.dataframe = pd.DataFrame(
            {
                hgvs_nt_column: ["c.1A>G"],
                hgvs_pro_column: ["p.Leu5Glu"],
                hgvs_splice_column: ["c.1A>G"],
                required_score_column: [1.000],
            }
        )

    def test_valid_column_names(self):
        validate_column_names(self.dataframe.columns)

    def test_missing_hgvs_column(self):
        self.dataframe = self.dataframe.drop([hgvs_nt_column, hgvs_pro_column, hgvs_splice_column], axis=1)
        with self.assertRaises(ValidationError):
            validate_column_names(self.dataframe.columns)

    def test_hgvs_in_wrong_location(self):
        self.dataframe = self.dataframe[[hgvs_nt_column, required_score_column, hgvs_pro_column, hgvs_splice_column]]
        with self.assertRaises(ValidationError):
            validate_column_names(self.dataframe.columns)

    def test_no_additional_columns_beyond_hgvs(self):
        self.dataframe = self.dataframe.drop([hgvs_pro_column, hgvs_splice_column, required_score_column], axis=1)
        with self.assertRaises(ValidationError):
            validate_column_names(self.dataframe.columns)

    def test_null_column_name(self):
        self.dataframe.rename(columns={hgvs_splice_column: 'null'}, inplace=True)
        with self.assertRaises(ValidationError):
            validate_column_names(self.dataframe.columns)


class TestValidateVariants(TestCase):
    def setUp(self):
        self.dataframe = pd.DataFrame(
            {
                hgvs_nt_column: ["c.1A>G", "c.1A>G", "c.1A>G"],
                hgvs_pro_column: ["p.Leu5Glu", "p.Leu5Glu", "p.Leu5Glu"],
                hgvs_splice_column: ["c.1A>G", "c.1A>G", "c.1A>G"],
            }
        )

    def test_valid_variants(self):
        validate_variants(self.dataframe["hgvs_nt"])

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
    def setUp(self):
        self.scores = pd.DataFrame(
            {
                hgvs_nt_column: ["c.1A>G"],
                hgvs_pro_column: ["p.Leu5Glu"],
                hgvs_splice_column: ["c.1A>G"],
            }
        )
        self.counts = pd.DataFrame(
            {
                hgvs_nt_column: ["c.1A>G"],
                hgvs_pro_column: ["p.Leu5Glu"],
                hgvs_splice_column: ["c.1A>G"],
            }
        )

    def test_valid(self):
        validate_dataframes_define_same_variants(self.scores, self.counts)

    def test_counts_defines_different_nt_variants(self):
        self.counts[hgvs_nt_column][0] = "c.2A>G"
        with self.assertRaises(ValidationError):
            validate_dataframes_define_same_variants(self.scores, self.counts)

    def test_counts_defines_different_splice_variants(self):
        self.counts[hgvs_splice_column][0] = "c.2A>G"
        with self.assertRaises(ValidationError):
            validate_dataframes_define_same_variants(self.scores, self.counts)

    def test_counts_defines_different_pro_variants(self):
        self.counts[hgvs_pro_column][0] = "p.Leu75Glu"
        with self.assertRaises(ValidationError):
            validate_dataframes_define_same_variants(self.scores, self.counts)