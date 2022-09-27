from numpy.testing import assert_array_equal
from pandas.testing import assert_frame_equal
from mavehgvs import Variant
from mavecore.validation.constants.general import *
from mavecore.validation.exceptions import ValidationError
from mavecore.validation.variant import validate_hgvs_string
from mavecore.validation.utilities import construct_hgvs_pro, get_codon_data_from_nt_variants
from mavecore.validation.constants.conversion import codon_dict_DNA


def validate_dataframes(target_seq, scores, counts=None):
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
    dataframe: pandas.DataFrame
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
    # also make sure counts df has a counts column
    if scores and not score_column:
        raise ValidationError("A scores dataframe must include a `score` column.")
    if not scores and score_column:
        raise ValidationError("A counts dataframe should not include a `score` column, include `score` "
                              "column in a scores dataframe.")


def validate_values_by_column(dataset, target_seq):
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
            validate_hgvs_string(value=dataset.loc[i, hgvs_nt_column],
                                 column="nt",
                                 targetseq=target_seq)
        if hgvs_pro:
            validate_hgvs_string(value=dataset.loc[i, hgvs_pro_column],
                                 column="p",
                                 targetseq=target_seq)
        if hgvs_splice:
            validate_hgvs_string(value=dataset.loc[i, hgvs_splice_column],
                                 column="splice",
                                 targetseq=target_seq)
        if score:
            validate_score(dataset.loc[i, required_score_column])
        if hgvs_nt and hgvs_pro:
            validate_hgvs_columns_define_same_variants(target_seq=target_seq,
                                                       nt=dataset.loc[i, hgvs_nt_column],
                                                       pro=dataset.loc[i, hgvs_pro_column],
                                                       row=i)

    # make sure target seq is the right type
    # no protein target with just nt variants


def validate_score(score):
    if type(score) != float:
        raise ValidationError(
            "Each value in score column must by a float. "
            "'{}' has the type '{}'.".format(score, type(score).__name__)
        )


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
