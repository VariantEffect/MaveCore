from constants.urn import *
from mavecore.validation.exceptions import ValidationError


def validate_urn(urn):
    """
    This function validates a MaveDB urn and raises an error if it is not valid.

    Parameters
    __________
    urn : str
        The MaveDB urn to be validated.

    Raises
    ______
    ValidationError
        If the MaveDB urn is not valid.
    """
    if not MAVEDB_ANY_URN_RE.match(urn):
        raise ValidationError("{}'s is not a valid urn.".format(urn))


def validate_experimentset_urn(urn):
    """
    This function validates a Experiment Set urn and raises an error if it is not valid.

    Parameters
    __________
    urn : str
        The Experiment Set urn to be validated.

    Raises
    ______
    ValidationError
        If the Experiment Set urn is not valid.
    """
    if not (MAVEDB_EXPERIMENTSET_URN_RE.match(urn) or MAVEDB_TMP_URN_RE.match(urn)):
        raise ValidationError(
            # "Error test"
            "{}'s is not a valid Experiment Set urn.".format(urn)
        )


def validate_experiment_urn(urn):
    """
    This function validates an Experiment urn and raises an error if it is not valid.

    Parameters
    __________
    urn : str
        The Experiment urn to be validated.

    Raises
    ______
    ValidationError
        If the Experiemnt urn is not valid.
    """
    if not (MAVEDB_EXPERIMENT_URN_RE.match(urn) or MAVEDB_TMP_URN_RE.match(urn)):
        raise ValidationError(
            "{}'s is not a valid Experiment urn.".format(urn)
        )


def validate_scoreset_urn(urn):
    """
    This function validates a Scoreset urn and raises an error if it is not valid.

    Parameters
    __________
    urn : str
        The Scoreset urn to be validated

    Raises
    ______
    ValidationError
        If the Scoreset urn is not valid.
    """
    if not (MAVEDB_SCORESET_URN_RE.match(urn) or MAVEDB_TMP_URN_RE.match(urn)):
        raise ValidationError("{}'s is not a valid score set urn.".format(urn))


def validate_variant_urn(urn):
    """
    This function validates a MaveDB Variant urn and raises an error if it is not valid.

    Parameters
    __________
    urn : str
        The MaveDB Variant urn to be validated.

    Raises
    ______
    ValidationError
        If the MaveDB Variant urn is not valid.
    """
    if not (MAVEDB_VARIANT_URN_RE.match(urn) or MAVEDB_TMP_URN_RE.match(urn)):
        raise ValidationError("{}'s is not a valid Variant urn.".format(urn))
