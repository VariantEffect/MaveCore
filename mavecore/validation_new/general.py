from exceptions import ValidationError
import datetime


def validate_data_usage_policy(dataUsagePolicy):
    """
    Validates
    :param dataUsagePolicy:
    :return:
    """


def validate_license_id(licenseId):
    """

    :param licenseId:
    :return:
    """


def validate_replaces_id(replacesId):
    """

    :param replacesId:
    :return:
    """


def validate_processing_state(processingState):
    """

    :param processingState:
    :return:
    """
    return


def validate_date(date):
    """
    Validates a date such as creation date, modification date and published date.

    Parameters:
    __________
    date: str
        The date to be validated.

    Raises:
    ______
    ValidationError
        If the date is in the wrong format.
    """
    template = '%Y-%m-%d'
    try:
        datetime.datetime.strptime(date, template)
    except ValidationError:
        print("Date should be formatted as YYYY-MM-DD")


def validate_private(private):
    """
    Validate private attribute.

    Parameters:
    __________
    private: bool
        The boolean private attribute to be validated.

    Raises:
    ______
    ValidationError
        If the private attribute is not a bool.
    """
    if type(private) != bool: raise ValidationError("The private attribute should be of type boolean.")