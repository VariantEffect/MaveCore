from numpy.testing import assert_array_equal
from pandas.testing import assert_frame_equal
from mavehgvs import Variant
from mavecore.validation.constants.general import *
from mavecore.validation.exceptions import ValidationError
from mavecore.validation.variant import validate_hgvs_string


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
    hgvs_columns = validate_column_names(scores.columns)
    for column in hgvs_columns:
        validate_variants(scores[column])
    if counts is not None:
        validate_no_null_columns_or_rows(counts)
        hgvs_columns = validate_column_names(counts.columns)
        for column in hgvs_columns:
            validate_variants(counts[column])
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
    # count instances of hgvs columns
    count = 0
    for i in range(len(columns)):
        # there should not be any null columns
        if columns[i] in readable_null_values_list: raise ValidationError("Column names must not be null.")
        if columns[i] in [hgvs_nt_column, hgvs_pro_column, hgvs_splice_column]: count+=1
    # there should be at least one hgvs column
    if count == 0: raise ValidationError("Must include hgvs_nt, hgvs_pro, or hgvs_splice column.")
    # first columns should be hgvs columns
    for i in range(count):
        if columns[i] not in [hgvs_nt_column, hgvs_pro_column, hgvs_splice_column]:
            raise ValidationError("First columns must be hgvs columns.")
    # there should be at least one additional column beyond the hgvs columns
    if len(columns) == count:
        raise ValidationError("There must be at least one additional column beyond the hgvs columns.")
    # validate against UTF-8byte ordering marks
    # TODO if dataframe is a scores df make sure it has a score column


def validate_variants(variants, column_name=None):
    """
    Validates a string of variants and verifies that the variant type in the column name makes
    sense with regards to the actual variants.

    Parameters
    __________
    variants: list[str]
        List of mavehgvs formatted strings.
    column_name: str
        The hgvs column name from which the variants parameter originates.

    Raises
    ______
    ValidationError
        If any variant in the list of variants does not adhere to the mavehgvs specifications.
    """
    # variant strings will be cast into hgvs variant objects to validate
    for variant in variants:
        if column_name == "hgvs_nt":
            column = "nt"
        elif column_name == "hgvs_pro":
            column = "p"
        elif column_name == "hgvs_splice":
            column = "splice"
        validate_hgvs_string(variant, column=column)
        '''try:
            v = Variant(variant)
            # variants should align with the hgvs column names
            # check this by seeing if the prefix makes sense with regards to the hgvs column name
            validate_variant_matches_hgvs_column_name(column_name, v.prefix)
        except ValidationError:
            raise ValidationError(variant + " does not adhere to mavehgvs variant guidelines.")


def validate_variant_matches_hgvs_column_name(variant, column_name):
    """
    Checks that a variant makes sense with regards to the hgvs column name.

    Parameters
    __________
    variants: list[str]
        List of mavehgvs formatted strings.
    column_name: str
        The hgvs column name from which the variants parameter originates.

    Raises
    ______
    ValidationError
        If the variant does not make sense with regards to the hgvs column name.
    """
    pass


def validate_hgvs_columns_define_same_variants(nt=None, pro=None):
    """
    Checks that, when two or more of hgvs_nt, hgvs_pro, and hgvs_splice columns exist, the variant strings within
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
