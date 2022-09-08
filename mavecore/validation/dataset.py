from numpy.testing import assert_array_equal
from pandas.testing import assert_frame_equal
from mavehgvs import Variant
from mavecore.validation.constants.general import *
from mavecore.validation.exceptions import ValidationError


def validate_dataframes(scores=None, counts=None):
    """
    Validates scores and counts dataframes for MaveDB upload. This function performs
    comprehensive validation.

    Parameters
    __________
    scores: pandas.DataFrame
        The scores data as a pandas dataframe.
    counts: pandas.DataFrame
        The counts data as a pandas dataframe.

    Raises
    ______
    ValidationError
        If any of the validation fails.
    """
    validate_no_null_columns_or_rows(scores)
    validate_column_names(scores.columns)
    validate_variants(scores)
    if counts is not None:
        validate_no_null_columns_or_rows(counts)
        validate_column_names(counts.columns)
        validate_variants(counts)
        validate_dataframes_define_same_variants(scores, counts)


def validate_no_null_columns_or_rows(dataframe):
    """
    Checks that there are no null columns or rows in the dataframe. Note that a null
    column may still have a valid column name.

    Parameters
    __________
    dataframe: pandas.DataFrame
        The scores or counts dataframe being validated

    Raises
    ______
    ValidationError
        If there are null columns or rows in the dataframe
    """
    df = dataframe.dropna(axis=0, how='all')
    df = df.dropna(axis=1, how='all')
    try:
        assert_frame_equal(df, dataframe)
    except AssertionError:
        raise ValidationError("Dataset should not contain null columns or rows.")


def validate_column_names(columns):
    """
    This function validates the columns in a dataframe. The first columns should be
    an hgvs column such as hgvs_nt, hgvs_pro, and hgvs_splice. There should be at least
    one column beyond the hgvs columns. A scores dataframe should have a score column and
    a counts dataframe should have a counts column. There should not be any null columns.
    The column names will also be validated against unusual file conversions that could
    corrupt the column names.

    Parameters
    __________
    dataframe: pandas.DataFrame
        The scores or counts dataframe to be validated.

    Raises
    ______
    ValidationError
        If the column names are not formatted correctly.
    """
    # first columns should be hgvs columns
    # there should be at least one additional column beyond the hgvs columns
    # there should not be any null columns
    # validate against UTF-8byte ordering marks
    pass


def validate_variants(dataframe):
    """

    :param dataframe:
    :return:
    """
    # variant strings will be cast into hgvs variant objects to validate
    # variants should align with the hgvs column names
    pass


def validate_variants_match_hgvs_column_name(dataframe):
    """

    :param dataframe:
    :return:
    """
    pass


def validate_hgvs_columns_define_same_variants(nt=None, pro=None):
    """
    Checks that, when both hgvs_nt and hgvs_pro columns exist, the variant strings within
    those columns are representing the same change.

    Parameters
    __________
    nt: list
        The hgvs_nt column represented as a list.
    pro: list
        The hgvs_pro column represented as a list.

    Raises
    ______
    ValidationError
        If any of the variants within each column do not represent the same change.
    """
    pass


def validate_dataframes_define_same_variants(scores, counts):
    """
    Checks if two `pd.DataFrame` objects parsed from uploaded files
    define the same variants.

    Parameters
    ----------
    scores: pandas.DataFrame
        Scores dataframe parsed from an uploaded scores file.
    counts: pandas.DataFrame
        Scores dataframe parsed from an uploaded counts file.

    Raises
    ______
    ValidationError
        If score and counts files do not define the same variants.
    """
    try:
        assert_array_equal(
            scores[hgvs_nt_column].sort_values().values,
            counts[hgvs_nt_column].sort_values().values,
        )
        assert_array_equal(
            scores[hgvs_splice_column].sort_values().values,
            counts[hgvs_splice_column].sort_values().values,
        )
        assert_array_equal(
            scores[hgvs_pro_column].sort_values().values,
            counts[hgvs_pro_column].sort_values().values,
        )
    except AssertionError:
        raise ValidationError(
            "Your score and counts files do not define the same variants. "
            "Check that the hgvs columns in both files match."
        )
