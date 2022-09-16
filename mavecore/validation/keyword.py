from mavecore.validation.exceptions import ValidationError
from mavecore.validation.utilities import is_null


def validate_keywords(v):
    if is_null(v):
        raise ValidationError("{} are not valid keywords. Keywords must be a valid list of strings.".format(v))
    else:
        for keyword in v:
            if is_null(keyword) or not isinstance(keyword, str):
                raise ValidationError("{} not a valid keyword. Keywords must be valid strings.".format(keyword))


def validate_keyword(kw):
    """
    This function validates whether or not the kw parameter is valid by
    checking that it is a string that is not null. If kw is null
    or is not a string, an error is raised.

    Parameters
    __________
    kw : str
        The keyword to be validated.

    Raises
    ______
    ValidationError
        If the kw argument is not a valid string.
    """
    if is_null(kw) or not isinstance(kw, str):
        raise ValidationError(
            f"'{kw}' not a valid keyword. Keywords must be valid strings."
        )


def validate_keyword_list(values):
    """
    This function takes a list of keyword values and validates that each one is valid.
    A valid keyword is a non-null string. The validate_keyword function will raise an
    ValidationError if any of the keywords are invalid.

    Parameters
    __________
    values : list[str]
        The list of values to be validated.
    """
    for value in values:
        if not is_null(value):
            validate_keyword(value)