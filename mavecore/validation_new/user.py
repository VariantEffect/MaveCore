from exceptions import ValidationError
from type import *


def validate_user(userId):
    """
    This function validates a user ID.

    Parameters:
    __________
    id: dict
        The user ID as a dictionary of user attributes

    Raises:
    ______
    ValidationError
        If any of the user attributes are found to be invalid.
    """
    # check id type
    is_dictionary(userId)
    # run additional validation
    validate_orcid_id(userId.get("orcid_id"))
    validate_first_name(userId.get("first_name"))
    validate_last_name(userId.get("lastName"))
    validate_email(userId.get("email"))


def validate_orcid_id(orcid_id):
    """
    Validates ORCID ID.

    Parameters:
    __________
    orcid_id: str
        The user's ORCID ID.

    Raises:
    ______
    ValidationError
        If the user's ORCID ID is not valid.
    """
    # check type
    is_string(orcid_id)


def validate_first_name(firstName):
    """
    Validates user's first name.

    Parameters:
    __________
    firstName: str
        The user's first name.

    Raises:
    ______
    ValidationError
        If the user's first name is not a string.
    """
    # check type
    is_string(firstName)


def validate_last_name(lastName):
    """
    Validates user's last name.

    Parameters:
    __________
    lastName: str
        The user's last name.

    Raises:
    ______
    ValidationError
        If the user's last name is not a string.
    """
    # check type
    is_string(lastName)


def validate_email(email):
    """
    Validates user's email.

    Parameters:
    __________
    email: str
        The user's email.

    Raises:
    ______
    ValidationError
        If the user's email is not valid.
    """
    # check type
    is_string(email)
