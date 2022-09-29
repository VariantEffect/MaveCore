from numpy.testing import assert_array_equal
from pandas.testing import assert_frame_equal
from mavehgvs.variant import Variant

from mavecore.validation.constants.general import (
    readable_null_values_list,
    hgvs_nt_column,
    hgvs_pro_column,
    hgvs_splice_column,
    required_score_column
)
from mavecore.validation.exceptions import ValidationError
from mavecore.validation.variant import validate_nt_variant, validate_pro_variant, validate_splice_variant
from mavecore.validation.utilities import convert_hgvs_nt_to_hgvs_pro


def validate_dataframes(target_seq: str, scores, counts=None):
    """
    Validates scores and counts dataframes for MaveDB upload. This function performs
    comprehensive validation.

    Parameters
    __________
    scores : pandas.DataFrame
        The scores data as a pandas dataframe.
    counts : pandas.DataFrame
        The counts data as a pandas dataframe.

    Raises
    ______
    ValidationError
        If any of the validation fails.
    """
    validate_no_null_columns_or_rows(scores)
    validate_column_names(scores.columns)
    validate_values_by_column(scores, target_seq)
    if counts is not None:
        validate_no_null_columns_or_rows(counts)
        validate_column_names(counts.columns, scores=False)
        validate_values_by_column(counts, target_seq)
        validate_dataframes_define_same_variants(scores, counts)


def validate_no_null_columns_or_rows(dataframe):
    """
    Checks that there are no null columns or rows in the dataframe. Note that a null
    column may still have a valid column name.

    Parameters
    __________
    dataframe : pandas.DataFrame
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


def validate_column_names(columns, scores=True):
    """
    This function validates the columns in a dataframe. The first columns should be
    an hgvs column such as hgvs_nt, hgvs_pro, and hgvs_splice. There should be at least
    one column beyond the hgvs columns. A scores dataframe should have a score column and
    a counts dataframe should have a counts column. There should not be any null columns.
    The column names will also be validated against unusual file conversions that could
    corrupt the column names.

    Parameters
    __________
    dataframe : pandas.DataFrame
        The scores or counts dataframe to be validated.

    Raises
    ______
    ValidationError
        If the column names are not formatted correctly.
    """
    # count instances of hgvs columns
    count = 0
    score_column = False
    for i in range(len(columns)):
        # there should not be any null columns
        if columns[i] in readable_null_values_list: raise ValidationError("Column names must not be null.")
        if columns[i] in [hgvs_nt_column, hgvs_pro_column, hgvs_splice_column]: count+=1
        if columns[i] == required_score_column: score_column = True
    # there should be at least one hgvs column
    if count == 0:
        raise ValidationError("Must include hgvs_nt, hgvs_pro, or hgvs_splice column.")
    # first columns should be hgvs columns
    for i in range(count):
        if columns[i] not in [hgvs_nt_column, hgvs_pro_column, hgvs_splice_column]:
            raise ValidationError("First columns must be hgvs columns.")
    # there should be at least one additional column beyond the hgvs columns
    if len(columns) == count:
        raise ValidationError("There must be at least one additional column beyond the hgvs columns.")
    # if dataframe is a scores df make sure it has a score column
    # also make sure counts df has a counts column and not a score column
    if scores and not score_column:
        raise ValidationError("A scores dataframe must include a `score` column.")
    if not scores and score_column:
        raise ValidationError("A counts dataframe should not include a `score` column, include `score` "
                              "column in a scores dataframe.")


def validate_values_by_column(dataset, target_seq: str):
    """
    Validates that the values in each column labeled `hgvs_nt`, `hgvs_pro`, `hgvs_splice`, and `score` make sense
    with regards to their column name. It also validates via a helper function that if both an `hgvs_nt` column and
    an `hgvs_pro` column exist, they are consistent with one another.

    Parameters
    __________
    dataset : pandas.DataFrame
        A scores or counts dataframe.
    target_seq: str
        The hgvs column name from which the variants parameter originates.

    Raises
    ______
    ValidationError
        If the target sequence does not contain solely the bases ACTG.
    ValidationError
        If any variant fails validation or if the variants are not consistent with one another.
    """
    # check for ValueError
    # if target_seq is not made solely of characters ACTG
    check_chars = [letter in "ACTG" for letter in target_seq]
    if False in check_chars:
        raise ValidationError("target_seq is invalid, must be composed only of bases ACTG.")

    # first check the column names, establish the order or the hgvs and score columns
    hgvs_nt = False
    hgvs_pro = False
    hgvs_splice = False
    score = False
    for column in dataset.columns:
        if column == hgvs_nt_column:
            hgvs_nt = True
        elif column == hgvs_pro_column:
            hgvs_pro = True
        elif column == hgvs_splice_column:
            hgvs_splice = True
        elif column == required_score_column:
            score = True
        else:
            raise ValidationError("Missing required hgvs and/or score columns.")

    # loop through row by row, validate hgvs strings, make sure nt and pro are consistent with one another
    for i in range(len(dataset)):
        if hgvs_nt:
            validate_nt_variant(value=dataset.loc[i, hgvs_nt_column],
                                targetseq=target_seq)
        if hgvs_pro:
            validate_pro_variant(value=dataset.loc[i, hgvs_pro_column],
                                 targetseq=target_seq)
        if hgvs_splice:
            validate_splice_variant(value=dataset.loc[i, hgvs_splice_column],
                                    targetseq=target_seq)
        if score:
            validate_score(dataset.loc[i, required_score_column])
        if hgvs_nt and not Variant(hgvs_pro).is_multi_variant():  # can only convert to single hgvs_pro variants
            validate_hgvs_nt_and_hgvs_pro_represent_same_change(target_seq=target_seq,
                                                                nt=dataset.loc[i, hgvs_nt_column],
                                                                pro=dataset.loc[i, hgvs_pro_column],
                                                                row=i)

    # make sure target seq is the right type
    # no protein target with just nt variants


def validate_score(score: float):
    # TODO we probably dont need this
    if type(score) != float:
        raise ValidationError(
            "Each value in score column must by a float. "
            "'{}' has the type '{}'.".format(score, type(score).__name__)
        )


def validate_hgvs_nt_and_hgvs_pro_represent_same_change(target_seq: str, nt: str, pro: str, row: int):
    """
    Checks that, when both an `hgvs_nt` and an `hgvs_pro` exist, the variant strings within
    those columns are representing the same change.

    Parameters
    __________
    target_seq : str
        The target sequence associated withe variants.
    nt : str
        The hgvs_nt string.
    pro : list
        The hgvs_pro string.

    Raises
    ______
    ValidationError
        If the variants do not represent the same change.
    """
    nt_converted = convert_hgvs_nt_to_hgvs_pro(nt, target_seq)
    # compare nt_converted with pro
    if nt_converted != pro:
        raise ValidationError("The hgvs_nt variant {} and the hgvs_pro variant {} on row {} do not represent the "
                              "same change.".format(nt, pro, row))


def validate_dataframes_define_same_variants(scores, counts):
    """
    Checks if two `pd.DataFrame` objects parsed from uploaded files
    define the same variants.

    Parameters
    ----------
    scores : pandas.DataFrame
        Scores dataframe parsed from an uploaded scores file.
    counts : pandas.DataFrame
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
