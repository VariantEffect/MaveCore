from mavecore.validation.exceptions import ValidationError
from mavecore.validation.utilities import is_null


def validate_keywords(v):
    if is_null(v):
        raise ValidationError("{} are not valid keywords. Keywords must be a non null list of strings.".format(v))
    else:
        for keyword in v:
            validate_keyword(keyword)


def validate_keyword(keyword: str):
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
    if is_null(keyword) or not isinstance(keyword, str):
        raise ValidationError("{} not a valid keyword. Keywords must be non null strings.".format(keyword))

