from unittest import TestCase
import numpy as np
import pandas as pd

from mavecore.validation.exceptions import ValidationError

from mavecore.validation.constants.general import (
    hgvs_nt_column,
    hgvs_pro_column,
    hgvs_splice_column,
    required_score_column
)

from mavecore.validation.dataframe import (
    validate_no_null_columns_or_rows,
    validate_column_names,
    validate_values_by_column,
    validate_score,
    validate_dataframes_define_same_variants
)
from mavecore.validation.constants.general import null_values_list

"""
from io import BytesIO, StringIO

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

    def test_valid_scores_column_names(self):
        validate_column_names(self.dataframe)

    def test_valid_counts_column_names(self):
        self.dataframe = self.dataframe.drop([required_score_column], axis=1)
        self.dataframe["count"] = [5]
        validate_column_names(self.dataframe, scores=False)

    def test_valid_just_hgvs_nt_hgvs_column(self):
        self.dataframe = self.dataframe.drop([hgvs_pro_column, hgvs_splice_column], axis=1)
        validate_column_names(self.dataframe)

    def test_valid_just_hgvs_pro_hgvs_column(self):
        self.dataframe = self.dataframe.drop([hgvs_nt_column, hgvs_splice_column], axis=1)
        validate_column_names(self.dataframe)

    def test_primary_column_is_pro_when_nt_is_not_defined(self):
        self.dataframe = self.dataframe.drop([hgvs_nt_column, hgvs_splice_column], axis=1)
        self.dataframe.insert(0, hgvs_splice_column, ["c.1A>G"], True)
        self.dataframe = validate_column_names(self.dataframe)
        self.assertTrue(self.dataframe.columns[0] == hgvs_pro_column)

    def test_missing_hgvs_column(self):
        self.dataframe = self.dataframe.drop([hgvs_nt_column, hgvs_pro_column, hgvs_splice_column], axis=1)
        with self.assertRaises(ValidationError):
            validate_column_names(self.dataframe)

    def test_hgvs_in_wrong_location(self):
        self.dataframe = self.dataframe[[hgvs_nt_column, required_score_column, hgvs_pro_column, hgvs_splice_column]]
        validate_column_names(self.dataframe) # validation fixes problem, should pass

    def test_no_additional_columns_beyond_hgvs_scores_df(self):
        self.dataframe = self.dataframe.drop([hgvs_pro_column, hgvs_splice_column, required_score_column], axis=1)
        with self.assertRaises(ValidationError):
            validate_column_names(self.dataframe)

    def test_no_additional_columns_beyond_hgvs_counts_df(self):
        self.dataframe = self.dataframe.drop([hgvs_pro_column, hgvs_splice_column, required_score_column], axis=1)
        with self.assertRaises(ValidationError):
            validate_column_names(self.dataframe, scores=False)

    def test_hgvs_columns_must_be_lowercase(self):
        self.dataframe.rename(columns={hgvs_nt_column: hgvs_nt_column.upper()}, inplace=True)
        with self.assertRaises(ValueError):
            validate_column_names(self.dataframe)

    def test_null_column_name(self):
        for value in null_values_list:
            self.dataframe.rename(columns={hgvs_splice_column: value}, inplace=True)
            with self.assertRaises(ValidationError):
                validate_column_names(self.dataframe)

    def test_no_score_column_with_scores_df(self):
        self.dataframe = self.dataframe.drop([required_score_column], axis=1)
        self.dataframe["count"] = [1]
        with self.assertRaises(ValidationError):
            validate_column_names(self.dataframe)

    def test_no_additional_column_with_counts_df(self):
        self.dataframe = self.dataframe.drop([required_score_column], axis=1)
        with self.assertRaises(ValidationError):
            validate_column_names(self.dataframe, scores=False)

    def test_invalid_missing_either_required_hgvs_column(self):
        self.dataframe = self.dataframe.drop([hgvs_pro_column, hgvs_nt_column], axis=1)
        with self.assertRaises(ValidationError):
            validate_column_names(self.dataframe, scores=False)

    def test_sort_column_names(self):
        self.dataframe = pd.DataFrame(
            {
                "other": 5,
                required_score_column: [1.000],
                hgvs_splice_column: ["c.1A>G"],
                hgvs_pro_column: ["p.Leu5Glu"],
                hgvs_nt_column: ["c.1A>G"],
            }
        )
        dataset = validate_column_names(self.dataframe)
        self.assertTrue(dataset.columns[0] == hgvs_nt_column)
        self.assertTrue(dataset.columns[1] == hgvs_pro_column)
        self.assertTrue(dataset.columns[2] == hgvs_splice_column)
        self.assertTrue(dataset.columns[3] == required_score_column)


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


class TestValidateValuesByColumn(TestCase):
    def setUp(self):
        self.target_seq = "ACA"
        self.dataframe = pd.DataFrame(
            {
                hgvs_nt_column: ["c.1A>G"],
                hgvs_pro_column: ["p.Thr1Ala"],
                hgvs_splice_column: ["c.1A>G"],
                required_score_column: [1.000],
            }
        )

    def test_non_numeric_values_in_score_column(self):
        self.dataframe[required_score_column][0] = "not a float"
        with self.assertRaises(ValidationError):
            validate_values_by_column(self.dataframe, target_seq=self.target_seq)

    def test_invalid_row_hgvs_is_not_a_string(self):
        self.dataframe[hgvs_nt_column][0] = 1.0
        with self.assertRaises(ValidationError):
            validate_values_by_column(self.dataframe, target_seq=self.target_seq)

    def test_empty_no_variants_parsed(self):
        self.dataframe = self.dataframe.drop(axis='rows', index=0)
        with self.assertRaises(ValidationError):
            validate_values_by_column(self.dataframe, target_seq=self.target_seq)

    def test_invalid_hgvs_in_column(self):
        # invalid hgvs_nt
        nt_test = self.dataframe.drop([hgvs_pro_column, hgvs_splice_column], axis=1)
        nt_test[hgvs_nt_column][0] = "p.Thr1Ala"
        with self.assertRaises(ValidationError):
            validate_values_by_column(nt_test, target_seq=self.target_seq)
        # invalid hgvs_pro
        pro_test = self.dataframe.drop([hgvs_nt_column, hgvs_splice_column], axis=1)
        pro_test[hgvs_pro_column][0] = "c.1A>G"
        with self.assertRaises(ValidationError):
            validate_values_by_column(pro_test, target_seq=self.target_seq)
        # invalid hgvs_splice
        splice_test = self.dataframe.drop([hgvs_pro_column], axis=1)
        splice_test[hgvs_splice_column][0] = "g.1A>G"
        splice_test[hgvs_splice_column][0] = "g.1A>G"
        with self.assertRaises(ValidationError):
            validate_values_by_column(splice_test, target_seq=self.target_seq)

    def test_invalid_variants_do_not_represent_same_change(self):
        self.dataframe[hgvs_nt_column][0] = "c.3A>G"
        with self.assertRaises(ValidationError):
            validate_values_by_column(self.dataframe, target_seq=self.target_seq)

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
        pass

    def test_invalid_same_variant_defined_in_two_rows_in_hgvs_pro(self):
        '''hgvs = generate_hgvs(prefix="p")
        data = "{},{}\n{},1.0\n{},1.0".format(self.HGVS_PRO_COL, "count", hgvs, hgvs)

        dataset = MaveDataset.for_counts(StringIO(data))
        dataset.validate()

        self.assertFalse(dataset.is_valid)
        self.assertEqual(len(dataset.errors), 1)
        print(dataset.errors)'''

    def test_does_not_allow_wt_and_sy(self):
        self.dataframe[hgvs_nt_column][0] = "_wt"
        with self.assertRaises(ValidationError):
            validate_values_by_column(self.dataframe, target_seq=self.target_seq)
        self.dataframe[hgvs_nt_column][0] = "c.1A>G"
        self.dataframe[hgvs_pro_column][0] = "_sy"
        with self.assertRaises(ValidationError):
            validate_values_by_column(self.dataframe, target_seq=self.target_seq)

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


class TestValidateScore(TestCase):
    def test_valid_score(self):
        validate_score(1.1)

    def test_invalid_score(self):
        with self.assertRaises(ValidationError):
            validate_score("a")


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

"""
from io import StringIO

import pandas as pd
from pandas.testing import assert_index_equal

# from dataset import constants
from mavecore.validation import constants

from mavecore.validation.variant_validators import (
    MaveDataset,
)
"""


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
