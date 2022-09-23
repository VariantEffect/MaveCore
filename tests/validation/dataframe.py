from unittest import TestCase
import pandas as pd

from mavecore.validation.dataframe import *
from mavecore.validation.constants.general import null_values_list

"""
from io import BytesIO, StringIO
from unittest import TestCase


import pandas as pd

from mavecore.validation import constants

from mavecore.validation.dataset_validators import (
    validate_scoreset_count_data_input,
    validate_scoreset_score_data_input,
    validate_at_least_one_additional_column,
    validate_has_hgvs_in_header,
    validate_header_contains_no_null_columns,
    read_header_from_io,
    validate_scoreset_json,
    validate_datasets_define_same_variants,
)


"""


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
        pass #validate_variants(self.dataframe[hgvs_nt_column], hgvs_nt_column)

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


class TestNoNullInColumnsValidator(TestCase):
    """
    Tests to ensure that an input file contains no null values in the header
    such as '', None, null etc.
    """

    def test_raises_valuerror_when_null_values_in_column(self):
        '''for value in constants.null_values_list:
            file = BytesIO(
                "{},score,{}\n".format(constants.hgvs_nt_column, value).encode()
            )
            with self.assertRaises(ValueError):
                header = read_header_from_io(file)
                validate_header_contains_no_null_columns(header)'''

    def test_does_not_raise_valuerror_when_non_null_values_in_column(
        self,
    ):
        '''file = BytesIO("{},score\n".format(constants.hgvs_nt_column).encode())
        header = read_header_from_io(file)
        validate_header_contains_no_null_columns(header)  # Should pass'''


class TestAtLeastOneNumericColumnValidator(TestCase):
    """
    Tests to ensure that an input file contains at least two columns.
    """

    def test_raises_valuerror_when_less_than_2_values_in_column(self):
        '''file = BytesIO("{}\n".format(constants.hgvs_nt_column).encode())
        with self.assertRaises(ValueError):
            header = read_header_from_io(file)
            validate_at_least_one_additional_column(header)'''

    def test_does_not_raise_valuerror_2_or_more_values_in_column(self):
        '''file = BytesIO("{},score,count\n".format(constants.hgvs_nt_column).encode())
        header = read_header_from_io(file)
        validate_at_least_one_additional_column(header)  # Should pass

        file = BytesIO("{},score\n".format(constants.hgvs_nt_column).encode())
        header = read_header_from_io(file)
        validate_at_least_one_additional_column(header)  # Should pass'''


class TestHgvsInHeaderValidator(TestCase):
    """
    Tests that case-sensitive 'hgvs' is in the header of a file.
    """

    def test_raises_valuerror_when_neither_hgvs_col_in_column(self):
        '''file = BytesIO("score,count\n".encode())
        with self.assertRaises(ValueError):
            header = read_header_from_io(file)
            validate_has_hgvs_in_header(header)'''

    def test_hgvs_must_be_lowercase(self):
        '''file = BytesIO(
            "{},score,count\n".format(constants.hgvs_nt_column.upper()).encode()
        )
        with self.assertRaises(ValueError):
            header = read_header_from_io(file)
            validate_has_hgvs_in_header(header)'''

    def test_does_not_raise_valuerror_when_either_hgvs_in_column(self):
        '''file = BytesIO("{},score,count\n".format(constants.hgvs_nt_column).encode())
        header = read_header_from_io(file)
        validate_has_hgvs_in_header(header)  # Should pass

        file = BytesIO("{},score,count\n".format(constants.hgvs_pro_column).encode())
        header = read_header_from_io(file)
        validate_has_hgvs_in_header(header)  # Should pass'''


class TestValidateScoreCountsDefineSameVariants(TestCase):
    """
    Tests that an uploaded score/counts files define the same variants
    in both the _nt column and _pro column.
    """

    def test_ve_counts_defines_different_nt_variants(self):
        '''scores = pd.DataFrame(
            {
                constants.hgvs_nt_column: ["c.1A>G"],
                constants.hgvs_pro_column: [None],
                constants.hgvs_splice_column: [None],
            }
        )
        counts = pd.DataFrame(
            {
                constants.hgvs_nt_column: ["c.2A>G"],
                constants.hgvs_pro_column: [None],
                constants.hgvs_splice_column: [None],
            }
        )
        with self.assertRaises(ValueError):
            validate_datasets_define_same_variants(scores, counts)'''

    def test_ve_counts_defines_different_splice_variants(self):
        '''scores = pd.DataFrame(
            {
                constants.hgvs_nt_column: [None],
                constants.hgvs_splice_column: ["c.1A>G"],
                constants.hgvs_pro_column: [None],
            }
        )
        counts = pd.DataFrame(
            {
                constants.hgvs_nt_column: [None],
                constants.hgvs_splice_column: ["c.2A>G"],
                constants.hgvs_pro_column: [None],
            }
        )
        with self.assertRaises(ValueError):
            validate_datasets_define_same_variants(scores, counts)'''

    def test_ve_counts_defines_different_pro_variants(self):
        '''scores = pd.DataFrame(
            {
                constants.hgvs_nt_column: [None],
                constants.hgvs_splice_column: [None],
                constants.hgvs_pro_column: ["p.Leu5Glu"],
            }
        )
        counts = pd.DataFrame(
            {
                constants.hgvs_nt_column: [None],
                constants.hgvs_splice_column: [None],
                constants.hgvs_pro_column: ["p.Leu75Glu"],
            }
        )
        with self.assertRaises(ValueError):
            validate_datasets_define_same_variants(scores, counts)'''

    def test_passes_when_same_variants_defined(self):
        '''scores = pd.DataFrame(
            {
                constants.hgvs_nt_column: ["c.1A>G"],
                constants.hgvs_pro_column: ["p.Leu5Glu"],
                constants.hgvs_splice_column: ["c.1A>G"],
            }
        )
        counts = pd.DataFrame(
            {
                constants.hgvs_nt_column: ["c.1A>G"],
                constants.hgvs_pro_column: ["p.Leu5Glu"],
                constants.hgvs_splice_column: ["c.1A>G"],
            }
        )
        validate_datasets_define_same_variants(scores, counts)'''


class TestValidateScoreSetCountDataInputValidator(TestCase):
    """
    Tests that validation errors are thrown when an ill-formatted count data
    input file is supplied.
    """

    def test_raises_valuerror_when_hgvs_not_in_column(self):
        '''file = BytesIO("score,count\n".encode())
        with self.assertRaises(ValueError):
            validate_scoreset_count_data_input(file)'''

    def test_raises_valuerror_no_numeric_column(self):
        '''file = BytesIO("{}\n".format(constants.hgvs_nt_column).encode())
        with self.assertRaises(ValueError):
            validate_scoreset_count_data_input(file)'''

    def test_raises_valuerror_when_null_values_in_column(self):
        '''for value in constants.null_values_list:
            file = BytesIO(
                "{},score,{}\n".format(constants.hgvs_nt_column, value).encode()
            )
            with self.assertRaises(ValueError):
                validate_scoreset_count_data_input(file)'''


class TestValidateScoreSetScoreDataInputValidator(TestCase):
    """
    Tests that validation errors are thrown when an ill-formatted score data
    input file is supplied.
    """

    def test_raises_valuerror_when_hgvs_not_in_column(self):
        '''file = BytesIO("score,count\n".encode())
        with self.assertRaises(ValueError):
            validate_scoreset_score_data_input(file)'''

    def test_raises_valuerror_no_numeric_column(self):
        '''file = BytesIO("{}\n".format(constants.hgvs_nt_column).encode())
        with self.assertRaises(ValueError):
            validate_scoreset_score_data_input(file)'''

    def test_raises_valuerror_when_null_values_in_column(self):
        '''for value in constants.null_values_list:
            file = BytesIO(
                "{},score,{}\n".format(constants.hgvs_nt_column, value).encode()
            )
            with self.assertRaises(ValueError):
                validate_scoreset_score_data_input(file)'''

    def test_validatation_error_score_not_in_header(self):
        '''file = BytesIO("{},count\n".format(constants.hgvs_nt_column).encode())
        with self.assertRaises(ValueError):
            validate_scoreset_score_data_input(file)'''


class TestValidateScoreSetJsonValidator(TestCase):
    """
    Test to ensure that a scoreset json field is properly formatted.
    """

    def test_valueerror_unexptected_columns(self):
        '''field = {
            "extra_column": [],
            constants.score_columns: ["score"],
            constants.count_columns: [],
        }
        with self.assertRaises(ValueError):
            validate_scoreset_json(field)'''

    def test_valueerror_values_not_lists(self):
        '''field = {constants.score_columns: ["score"], constants.count_columns: {}}
        with self.assertRaises(ValueError):
            validate_scoreset_json(field)'''

    def test_valueerror_list_values_not_strings(self):
        '''field = {constants.score_columns: [b"score"], constants.count_columns: []}
        with self.assertRaises(ValueError):
            validate_scoreset_json(field)'''

    def test_valueerror_empty_score_columns(self):
        '''field = {constants.score_columns: [], constants.count_columns: []}
        with self.assertRaises(ValueError):
            validate_scoreset_json(field)'''

    def test_valueerror_missing_dict_columns(self):
        '''# constants.score_columns missing
        field = {constants.count_columns: []}
        with self.assertRaises(ValueError):
            validate_scoreset_json(field)

        # constants.count_columns missing
        field = {constants.score_columns: ["score"]}
        with self.assertRaises(ValueError):
            validate_scoreset_json(field)'''

    def test_valueerror_missing_header_columns(self):
        '''# constants.score_columns columns missing 'score'
        field = {constants.score_columns: ["hgvs"], constants.count_columns: []}
        with self.assertRaises(ValueError):
            validate_scoreset_json(field)'''


"""
from io import StringIO
import unittest
from unittest import TestCase
from random import choice

import pandas as pd
from pandas.testing import assert_index_equal

# from dataset import constants
from mavecore.validation import constants
from mavecore.validation.exceptions import ValidationError

from mavecore.validation.variant_validators import (
    MaveDataset,
)
"""

def generate_hgvs(prefix: str = "c") -> str:
    """'''Generates a random hgvs string from a small sample.'''"""
    '''if prefix == "p":
        # Subset of 3-letter codes, chosen at random.
        amino_acids = [
            "Ala",
            "Leu",
            "Gly",
            "Val",
            "Tyr",
            "Met",
            "Cys",
            "His",
            "Glu",
            "Phe",
        ]
        ref = choice(amino_acids)
        alt = choice(amino_acids)
        return f"{prefix}.{ref}{choice(range(1, 100))}{alt}"
    else:
        alt = choice("ATCG")
        ref = choice("ATCG")
        return f"{prefix}.{choice(range(1, 100))}{ref}>{alt}"'''



class TestMaveDataset(TestCase):
    """
    Tests the validator :func:`validate_variant_rows` to check if the correct
    errors are thrown when invalid rows are encountered in a
    scores/counts/meta data input file. Checks for:
        - Invalid HGVS string in a row
        - Row HGVS is defined in more than one row
        - Row values are not int/float for a count/score file

    Tests also check to see if the correct header and hgvs data information
    is parsed and returned.
    """

    '''SCORE_COL = constants.required_score_column
    HGVS_NT_COL = constants.hgvs_nt_column
    HGVS_SPLICE_COL = constants.hgvs_splice_column
    HGVS_PRO_COL = constants.hgvs_pro_column'''

    @staticmethod
    def mock_return_value(data, index=None):
        '''df = pd.read_csv(StringIO(data), sep=",", na_values=["None", None])
        if index:
            df.index = pd.Index(df[index])
        return df'''

    def test_invalid_row_hgvs_is_not_a_string(self):
        '''data = "{},{}\n1.0,1.0".format(self.HGVS_NT_COL, self.SCORE_COL)

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate()

        self.assertFalse(dataset.is_valid)
        self.assertEqual(len(dataset.errors), 1)
        print(dataset.errors)'''

    def test_invalid_missing_hgvs_columns(self):
        '''data = "{},{}\n{},1.0".format("not_hgvs", self.SCORE_COL, generate_hgvs())

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate()

        self.assertFalse(dataset.is_valid)
        self.assertEqual(len(dataset.errors), 1)
        print(dataset.errors)'''

    def test_replaces_null_with_none_in_secondary_hgvs_column(self):
        '''hgvs_nt = generate_hgvs(prefix="c")
        for c in constants.null_values_list:
            with self.subTest(msg=f"'{c}'"):
                data = "{},{},{}\n{},{},1.0 ".format(
                    self.HGVS_NT_COL, self.HGVS_PRO_COL, self.SCORE_COL, hgvs_nt, c
                )

                dataset = MaveDataset.for_scores(StringIO(data))
                dataset.validate()

                self.assertTrue(dataset.is_valid)
                self.assertListEqual(
                    list(dataset.data(serializable=True)[self.HGVS_PRO_COL]), [None]
                )'''

    def test_replaces_null_with_none_in_numeric_columns(self):
        '''hgvs_nt = generate_hgvs(prefix="c")
        for c in constants.null_values_list:
            with self.subTest(msg=f"'{c}'"):
                data = "{},{}\n{},{}".format(
                    self.HGVS_NT_COL, self.SCORE_COL, hgvs_nt, c
                )

                dataset = MaveDataset.for_scores(StringIO(data))
                dataset.validate()

                self.assertTrue(dataset.is_valid)
                self.assertListEqual(
                    list(dataset.data(serializable=True)[self.SCORE_COL]), [None]
                )'''

    def test_invalid_null_values_in_header(self):
        '''for value in constants.null_values_list:
            with self.subTest(msg=f"'{value}'"):
                data = "{},{},{}\n{},1.0,1.0".format(
                    self.HGVS_NT_COL, self.SCORE_COL, value, generate_hgvs()
                )

                dataset = MaveDataset.for_scores(StringIO(data))
                dataset.validate()

                self.assertFalse(dataset.is_valid)
                self.assertEqual(len(dataset.errors), 1)
                print(dataset.errors)'''

    def test_invalid_no_additional_columns_outside_hgvs_ones(self):
        '''data = "{},{},{}\n{},{},{}".format(
            self.HGVS_NT_COL,
            self.HGVS_SPLICE_COL,
            self.HGVS_PRO_COL,
            generate_hgvs(prefix="g"),
            generate_hgvs(prefix="c"),
            generate_hgvs(prefix="p"),
        )

        dataset = MaveDataset.for_counts(StringIO(data))
        dataset.validate()

        self.assertFalse(dataset.is_valid)
        self.assertEqual(len(dataset.errors), 1)
        print(dataset.errors)'''

    def test_scores_missing_scores_column(self):
        '''data = "{},{}\n{},{}".format(
            self.HGVS_NT_COL, "scores_rna", generate_hgvs(prefix="g"), 1.0
        )

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate()

        self.assertFalse(dataset.is_valid)
        self.assertEqual(len(dataset.errors), 1)
        print(dataset.errors)'''

    def test_invalid_missing_either_required_hgvs_column(self):
        '''data = "{},{}\n{},{}".format(
            self.HGVS_SPLICE_COL, self.SCORE_COL, generate_hgvs(prefix="c"), 1.0
        )

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate()

        self.assertFalse(dataset.is_valid)
        self.assertEqual(len(dataset.errors), 1)
        print(dataset.errors)'''

    def test_empty_no_variants_parsed(self):
        '''data = "{},{}\n".format(self.HGVS_NT_COL, self.SCORE_COL)

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate()

        self.assertTrue(dataset.is_empty)
        self.assertFalse(dataset.is_valid)
        self.assertEqual(len(dataset.errors), 1)
        print(dataset.errors)'''

    def test_error_non_numeric_values_in_score_column(self):
        '''data = "{},{}\n{},{}".format(
            self.HGVS_NT_COL,
            self.SCORE_COL,
            generate_hgvs(prefix="c"),
            "I am not a number",
        )

        with self.assertRaises(ValueError):
            MaveDataset.for_scores(StringIO(data))'''

    def test_invalid_same_hgvs_nt_defined_in_two_rows(self):
        '''hgvs = generate_hgvs(prefix="c")
        data = "{},{}\n{},1.0\n{},1.0".format(
            self.HGVS_NT_COL, self.SCORE_COL, hgvs, hgvs
        )

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate()

        self.assertFalse(dataset.is_valid)
        self.assertEqual(len(dataset.errors), 1)
        print(dataset.errors)'''

    def test_invalid_same_variant_defined_in_two_rows_in_hgvs_pro(self):
        '''hgvs = generate_hgvs(prefix="p")
        data = "{},{}\n{},1.0\n{},1.0".format(self.HGVS_PRO_COL, "count", hgvs, hgvs)

        dataset = MaveDataset.for_counts(StringIO(data))
        dataset.validate()

        self.assertFalse(dataset.is_valid)
        self.assertEqual(len(dataset.errors), 1)
        print(dataset.errors)'''

    def test_data_method_converts_null_values_to_None(self):
        '''hgvs = generate_hgvs()
        for value in constants.null_values_list:
            with self.subTest(msg=value):
                data = "{},{}\n{},{}".format(
                    self.HGVS_NT_COL, self.SCORE_COL, hgvs, value
                )

                dataset = MaveDataset.for_scores(StringIO(data))
                dataset.validate()

                self.assertTrue(dataset.is_valid)

                df = dataset.data(serializable=True)
                self.assertIsNotNone(df[self.HGVS_NT_COL].values[0])
                self.assertIsNone(df[self.SCORE_COL].values[0])'''

    def test_sorts_header(self):
        '''hgvs_nt = generate_hgvs(prefix="g")
        hgvs_pro = generate_hgvs(prefix="p")
        hgvs_splice = generate_hgvs(prefix="c")
        data = "{},{},{},{},{}\n{},{},{},{},{}".format(
            self.HGVS_PRO_COL,
            self.HGVS_NT_COL,
            "colA",
            self.SCORE_COL,
            self.HGVS_SPLICE_COL,
            hgvs_pro,
            hgvs_nt,
            "hello",
            1.0,
            hgvs_splice,
        )

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate()

        self.assertTrue(dataset.is_valid)
        self.assertListEqual(
            dataset.columns,
            [
                self.HGVS_NT_COL,
                self.HGVS_SPLICE_COL,
                self.HGVS_PRO_COL,
                self.SCORE_COL,
                "colA",
            ],
        )'''

    def test_does_not_allow_wt_and_sy(self):
        '''wt = "_wt"
        sy = "_sy"
        data = "{},{},{},{}\n{},{},{},1.0".format(
            self.HGVS_NT_COL,
            self.HGVS_SPLICE_COL,
            self.HGVS_PRO_COL,
            self.SCORE_COL,
            wt,
            wt,
            sy,
        )

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate()

        self.assertFalse(dataset.is_valid)
        self.assertEqual(len(dataset.errors), 3)
        print(dataset.errors)'''

    def test_parses_numeric_column_values_into_float(self):
        '''hgvs = generate_hgvs(prefix="c")
        data = "{},{}\n{},1.0".format(self.HGVS_NT_COL, self.SCORE_COL, hgvs)

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate()

        self.assertTrue(dataset.is_valid)
        value = dataset.data()[self.SCORE_COL].values[0]
        self.assertIsInstance(value, float)'''

    def test_does_not_split_double_quoted_variants(self):
        '''hgvs = "c.[123A>G;124A>G]"
        data = '{},{}\n"{}",1.0'.format(self.HGVS_NT_COL, self.SCORE_COL, hgvs)

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate()

        self.assertTrue(dataset.is_valid)
        self.assertIn(hgvs, dataset.data()[self.HGVS_NT_COL])

    # def test_invalid_non_double_quoted_multi_variant_row(self):
    #     hgvs = "{},{}".format(generate_hgvs(), generate_hgvs())
    #     data = "{},{}\n'{}',1.0".format(
    #         constants.hgvs_nt_column, required_score_column, hgvs
    #     )
    #     with self.assertRaises(ValidationError):
    #         _ = validate_variant_rows(BytesIO(data.encode()))'''

    def test_primary_column_is_pro_when_nt_is_not_defined(self):
        '''hgvs_pro = generate_hgvs(prefix="p")
        data = "{},{}\n{},1.0".format(self.HGVS_PRO_COL, self.SCORE_COL, hgvs_pro)

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate()

        self.assertTrue(dataset.is_valid)
        self.assertEqual(dataset.index_column, self.HGVS_PRO_COL)'''

    def test_primary_column_is_nt_by_default(self):
        '''hgvs_nt = generate_hgvs(prefix="c")
        hgvs_pro = generate_hgvs(prefix="p")
        data = "{},{},{}\n{},{},1.0".format(
            self.HGVS_NT_COL, self.HGVS_PRO_COL, self.SCORE_COL, hgvs_nt, hgvs_pro
        )

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate()

        self.assertTrue(dataset.is_valid)
        self.assertEqual(dataset.index_column, self.HGVS_NT_COL)'''

    def test_error_missing_value_in_nt_column_when_nt_is_primary(self):
        '''for v in constants.null_values_list:
            with self.subTest(msg=v):
                data = (
                    "{},{},{}\n"
                    "{},{},1.0\n"
                    "{},{},1.0".format(
                        self.HGVS_NT_COL,
                        self.HGVS_PRO_COL,
                        self.SCORE_COL,
                        generate_hgvs(prefix="c"),
                        generate_hgvs(prefix="p"),
                        v,
                        generate_hgvs(prefix="p"),
                    )
                )

                dataset = MaveDataset.for_scores(StringIO(data))
                dataset.validate()

                self.assertFalse(dataset.is_valid)
                self.assertEqual(len(dataset.errors), 1)
                print(dataset.errors)'''

    def test_error_missing_value_in_pro_column_when_pro_is_primary(self):
        '''for v in constants.null_values_list:
            with self.subTest(msg=v):
                data = "{},{}\n{},1.0\n{},1.0".format(
                    self.HGVS_PRO_COL, self.SCORE_COL, generate_hgvs(prefix="p"), v
                )

                dataset = MaveDataset.for_scores(StringIO(data))
                dataset.validate()

                self.assertFalse(dataset.is_valid)
                self.assertEqual(len(dataset.errors), 1)
                print(dataset.errors)'''

    def test_df_indexed_by_primary_column(self):
        '''data = "{},{},{}\n{},{},1.0".format(
            self.HGVS_NT_COL,
            self.HGVS_PRO_COL,
            self.SCORE_COL,
            generate_hgvs(prefix="c"),
            generate_hgvs(prefix="p"),
        )

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate()

        self.assertTrue(dataset.is_valid)
        assert_index_equal(dataset.data().index, dataset.index)'''

    def test_invalid_duplicates_in_index(self):
        '''hgvs = generate_hgvs(prefix="c")
        data = "{},{},{}\n{},{},1.0\n{},{},2.0".format(
            self.HGVS_NT_COL,
            self.HGVS_PRO_COL,
            self.SCORE_COL,
            hgvs,
            generate_hgvs(prefix="p"),
            hgvs,
            generate_hgvs(prefix="p"),
        )

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate()

        self.assertFalse(dataset.is_valid)
        self.assertEqual(len(dataset.errors), 1)
        print(dataset.errors)'''

    def test_invalid_hgvs_in_column(self):
        '''tests = [
            (self.HGVS_PRO_COL, generate_hgvs(prefix="c")),
            (self.HGVS_SPLICE_COL, generate_hgvs(prefix="g")),
            (self.HGVS_NT_COL, generate_hgvs(prefix="p")),
        ]
        for (column, variant) in tests:
            with self.subTest(msg=f"{column}: {variant}"):
                if column == self.HGVS_SPLICE_COL:
                    data = "{},{},{}\n{},{},1.0".format(
                        self.HGVS_NT_COL,
                        column,
                        self.SCORE_COL,
                        generate_hgvs(prefix="g"),
                        variant,
                    )
                else:
                    data = "{},{}\n{},1.0".format(column, self.SCORE_COL, variant)

                dataset = MaveDataset.for_scores(StringIO(data))
                dataset.validate()

                self.assertFalse(dataset.is_valid)
                self.assertEqual(len(dataset.errors), 1)
                print(dataset.errors)'''

    def test_invalid_genomic_and_transcript_mixed_in_nt_column(self):
        '''data = "{},{}\n{},1.0\n{},2.0".format(
            self.HGVS_NT_COL,
            self.SCORE_COL,
            generate_hgvs(prefix="g"),
            generate_hgvs(prefix="c"),
        )

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate()

        self.assertFalse(dataset.is_valid)
        self.assertEqual(len(dataset.errors), 2)
        print(dataset.errors)'''

    def test_invalid_nt_not_genomic_when_splice_present(self):
        '''data = "{},{},{}\n{},{},1.0".format(
            self.HGVS_NT_COL,
            self.HGVS_SPLICE_COL,
            self.SCORE_COL,
            generate_hgvs(prefix="c"),
            generate_hgvs(prefix="c"),
        )

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate()

        self.assertFalse(dataset.is_valid)
        self.assertEqual(len(dataset.errors), 1)
        print(dataset.errors)'''

    def test_invalid_splice_defined_when_nt_is_not(self):
        '''data = "{},{},{}\n,{},1.0".format(
            self.HGVS_NT_COL,
            self.HGVS_SPLICE_COL,
            self.SCORE_COL,
            generate_hgvs(prefix="c"),
        )

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate()

        self.assertFalse(dataset.is_valid)
        self.assertEqual(len(dataset.errors), 1)
        print(dataset.errors)'''

    def test_invalid_splice_not_defined_when_nt_is_genomic(self):
        '''data = "{},{}\n{},1.0".format(
            self.HGVS_NT_COL, self.SCORE_COL, generate_hgvs(prefix="g")
        )

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate()

        self.assertFalse(dataset.is_valid)
        self.assertEqual(len(dataset.errors), 2)
        print(dataset.errors)'''

    def test_invalid_zero_is_not_parsed_as_none(self):
        '''hgvs = generate_hgvs(prefix="c")
        data = "{},{}\n{},0.0".format(self.HGVS_NT_COL, self.SCORE_COL, hgvs)

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate()

        self.assertTrue(dataset.is_valid)
        df = dataset.data()
        self.assertEqual(df[self.SCORE_COL].values[0], 0)'''

    def test_invalid_close_to_zero_is_not_parsed_as_none(self):
        '''hgvs = generate_hgvs(prefix="c")
        data = "{},{}\n{},5.6e-15".format(self.HGVS_NT_COL, self.SCORE_COL, hgvs)

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate()

        self.assertTrue(dataset.is_valid)
        df = dataset.data()
        self.assertEqual(df[self.SCORE_COL].values[0], 5.6e-15)'''

    def test_defines_same_variants(self):
        '''tests = [
            (
                "{},{}\nc.1A>G,0.0".format(self.HGVS_NT_COL, self.SCORE_COL),
                "{},count\nc.1A>G,0.0".format(self.HGVS_NT_COL),
                True,
            ),
            (
                "{},{}\nc.1A>G,0.0".format(self.HGVS_NT_COL, self.SCORE_COL),
                "{},count\nc.2A>G,0.0".format(self.HGVS_NT_COL),
                False,
            ),
            (
                "{},{},{}\nc.1A>G,p.Ile1Val,0.0".format(
                    self.HGVS_NT_COL, self.HGVS_PRO_COL, self.SCORE_COL
                ),
                "{},{},count\nc.1A>G,p.Ile1Val,0.0".format(
                    self.HGVS_NT_COL, self.HGVS_PRO_COL
                ),
                True,
            ),
            (
                "{},{},{}\nc.1A>G,p.Ile1Val,0.0".format(
                    self.HGVS_NT_COL, self.HGVS_PRO_COL, self.SCORE_COL
                ),
                "{},{},count\nc.1A>G,p.Ile1Phe,0.0".format(
                    self.HGVS_NT_COL, self.HGVS_PRO_COL
                ),
                False,
            ),
            # Check returns None if either dataset invalid
            (
                "wrong_columns,{}\nc.1A>G,0.0".format(self.SCORE_COL),
                "{},count\nc.1A>G,0.0".format(self.HGVS_NT_COL),
                None,
            ),
            (
                "{},{}\nc.1A>G,0.0".format(self.HGVS_NT_COL, self.SCORE_COL),
                "wrong_column,count\nc.1A>G,0.0".format(),
                None,
            ),
        ]

        for (scores, counts, expected) in tests:
            with self.subTest(msg=(scores, counts, expected)):
                scores_dataset = MaveDataset.for_scores(StringIO(scores))
                scores_dataset.validate()

                counts_dataset = MaveDataset.for_counts(StringIO(counts))
                counts_dataset.validate()

                self.assertEqual(scores_dataset.match_other(counts_dataset), expected)'''

    def test_to_dict(self):
        '''hgvs_1 = generate_hgvs(prefix="c")
        hgvs_2 = generate_hgvs(prefix="c")
        data = "{},{},{},{}\n{},,,\n{},,,1.0".format(
            self.HGVS_NT_COL,
            self.HGVS_PRO_COL,
            self.HGVS_SPLICE_COL,
            self.SCORE_COL,
            hgvs_1,
            hgvs_2,
        )

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate()

        self.assertTrue(dataset.is_valid)
        self.assertDictEqual(
            dataset.to_dict(),
            {
                hgvs_1: {
                    self.HGVS_NT_COL: hgvs_1,
                    self.HGVS_SPLICE_COL: None,
                    self.HGVS_PRO_COL: None,
                    self.SCORE_COL: None,
                },
                hgvs_2: {
                    self.HGVS_NT_COL: hgvs_2,
                    self.HGVS_SPLICE_COL: None,
                    self.HGVS_PRO_COL: None,
                    self.SCORE_COL: 1.0,
                },
            },
        )'''

    def test_valid_targetseq_validation_fails(self):
        '''data = "{},{},{}\nc.1A>G,p.Ile1Val,0.5".format(
            self.HGVS_NT_COL, self.HGVS_PRO_COL, self.SCORE_COL
        )

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate(targetseq="ATC")

        self.assertTrue(dataset.is_valid)'''

    def test_invalid_targetseq_validation_fails(self):
        '''data = "{},{},{}\nc.1A>G,p.Val1Phe,0.5".format(
            self.HGVS_NT_COL, self.HGVS_PRO_COL, self.SCORE_COL
        )

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate(targetseq="ATC")

        self.assertFalse(dataset.is_valid)
        print(dataset.errors)

        self.assertEqual(dataset.n_errors, 1)
        self.assertIn("p.Val1Phe", dataset.errors[0])'''

    def test_invalid_target_sequence_not_a_multiple_of_3(self):
        '''data = "{},{},{}\nc.1A>G,p.Ile1Val,0.5".format(
            self.HGVS_NT_COL, self.HGVS_PRO_COL, self.SCORE_COL
        )

        dataset = MaveDataset.for_scores(StringIO(data))
        dataset.validate(targetseq="ATCG")

        self.assertFalse(dataset.is_valid)
        print(dataset.errors)

        self.assertEqual(dataset.n_errors, 1)
        self.assertIn("multiple of 3", dataset.errors[0])'''

    #@unittest.expectedFailure
    def test_invalid_relaxed_ordering_check_fails(self):
        '''self.fail("Test is pending")'''
