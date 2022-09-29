import idutils

from mavecore.validation.exceptions import ValidationError
from mavecore.validation.utilities import is_null
from mavecore.validation.constants.identifier import valid_dbnames


def validate_external_identifier(identifier: dict):
    """
    Validates an external identifier represented as a dictionary. The dictionary should have a length of 2
    and have the keys `dbname` and `identifier`, both with str values. The valid values for these keys are
    stored in lists within the identifier file in constants directory.

    Parameters
    __________
    identifier : dict
        The identifier to be validated.

    Raises
    ______
    ValidationError
        If the length of the dictionary is not 2.
    ValidationError
        If the keys do not have the correct name.
    ValidationError
        If the `dbname` value is not valid.
    ValidationError
        If the `identifier` value is not correct as it relates to the `dbname` value.
    """
    # check that identifier dict only has two keys
    if len(identifier) != 2:
        raise ValidationError("The identifier attribute of the external identifier should have two keys, `dbname` "
                              "and `identifier`.")

    # check that the keys are the right name
    if "dbname" not in identifier:
        raise ValidationError("The identifier attribute of the external identifier should have two Keys, `dbname` "
                              "and `identifier`.")
    if "identifier" not in identifier:
        raise ValidationError("The identifier attribute of the external identifier should have two Keys, `dbname` "
                              "and `identifier`.")

    # check that dbname is valid
    if identifier.get("dbname") not in valid_dbnames:
        raise ValidationError(f"The `dbname` key within the identifier attribute of the external identifier should "
                              f"take one of the following values: {valid_dbnames}.")

    # validate identifier based on dbname: could be one of UniProt, RefSeq, or Ensembl
    if identifier.get("dbname") == "UniProt":
        validate_uniprot_identifier(identifier.get("identifier"))
    elif identifier.get("dbname") == "RefSeq":
        validate_refseq_identifier(identifier.get("identifier"))
    elif identifier.get("dbname") == "Ensembl":
        validate_ensembl_identifier(identifier.get("identifier"))


def validate_sra_identifier(identifier: str):
    """
    Validates whether the identifier is a valid SRA identifier.

    Parameters
    __________
    identifier : str
        The identifier to be validated.

    Raises
    ______
    ValidationError
        If the identifier is not a valid SRA identifier.
    """
    if not (
        idutils.is_sra(identifier)
        or idutils.is_bioproject(identifier)
        or idutils.is_geo(identifier)
        or idutils.is_arrayexpress_array(identifier)
        or idutils.is_arrayexpress_experiment(identifier)
    ):
        raise ValidationError(
            f"'{identifier} is not a valid SRA, GEO, ArrayExpress or BioProject "
            "accession."
        )


def validate_pubmed_identifier(identifier: str):
    """
    Validates whether the identifier is a valid PubMed identifier.

    Parameters
    __________
    identifier : str
        The identifier to be validated.

    Raises
    ______
    ValidationError
        If the identifier is not a valid PubMed identifier.
    """
    if not idutils.is_pmid(identifier):
        #raise ValidationError(f"'{identifier} is not a valid PubMed identifier.")
        raise ValidationError("{} is not a valid PubMed identifier.".format(identifier))


def validate_doi_identifier(identifier: str):
    """
    Validates whether the identifier is a valid DOI identifier.

    Parameters
    __________
    identifier : str
        The identifier to be validated.

    Raises
    ______
    ValidationError
        If the identifier is not a valid DOI identifier.
    """
    if not idutils.is_doi(identifier):
        #raise ValidationError(f"'{identifier}' is not a valid DOI.")
        raise ValidationError("{} is not a valid DOI identifier.".format(identifier))


def validate_ensembl_identifier(identifier: str):
    """
    Validates whether the identifier is a valid Ensembl identifier.

    Parameters
    __________
    identifier : str
        The identifier to be validated.

    Raises
    ______
    ValidationError
        If the identifier is not a valid Ensembl identifier.
    """
    if not idutils.is_ensembl(identifier):
        raise ValidationError(f"'{identifier}' is not a valid Ensembl accession.")


def validate_uniprot_identifier(identifier: str):
    """
    Validates whether the identifier is a valid UniProt identifier.

    Parameters
    __________
    identifier : str
        The identifier to be validated.

    Raises
    ______
    ValidationError
        If the identifier is not a valid UniProt identifier.
    """
    if not idutils.is_uniprot(identifier):
        raise ValidationError(f"'{identifier}' is not a valid UniProt accession.")


def validate_refseq_identifier(identifier: str):
    """
    Validates whether the identifier is a valid RefSeq identifier.

    Parameters
    __________
    identifier : str
        The identifier to be validated.

    Raises
    ______
    ValidationError
        If the identifier is not a valid RefSeq identifier.
    """
    if not idutils.is_refseq(identifier):
        raise ValidationError(f"'{identifier}' is not a valid RefSeq accession.")


def validate_genome_identifier(identifier: str):
    """
    Validates whether the identifier is a valid genome identifier.

    Parameters
    __________
    identifier : str
        The identifier to be validated.

    Raises
    ______
    ValidationError
        If the identifier is not a valid genome identifier.
    """
    if not idutils.is_genome(identifier):
        raise ValidationError(
            f"'{identifier}' is not a valid GenBank or RefSeq genome assembly."
        )


def validate_pubmed_list(values: list[str]):
    """
    Validates whether each identifier in a list of identifiers (values) is a valid PubMed identifier.

    Parameters
    __________
    identifier : list[str]
        The list of identifiers to be validated.

    Raises
    ______
    ValidationError
        If at least one of the identifiers is not a valid PubMed identifier.
    """
    for value in values:
        if not is_null(value):
            validate_pubmed_identifier(value)


def validate_sra_list(values: list[str]):
    """
    Validates whether each identifier in a list of identifiers (values) is a valid SRA identifier.

    Parameters
    __________
    identifier : list[str]
        The list of identifiers to be validated.

    Raises
    ______
    ValidationError
        If at least one of the identifiers is not a valid SRA identifier.
    """
    for value in values:
        if not is_null(value):
            validate_sra_identifier(value)


def validate_doi_list(values: list[str]):
    """
    Validates whether each identifier in a list of identifiers (values) is a valid DOI identifier.

    Parameters
    __________
    identifier : list[str]
        The list of identifiers to be validated.

    Raises
    ______
    ValidationError
        If at least one of the identifiers is not a valid DOI identifier.
    """
    for value in values:
        if not is_null(value):
            validate_doi_identifier(value)


def validate_ensembl_list(values: list[str]):
    """
    Validates whether each identifier in a list of identifiers (values) is a valid Ensembl identifier.

    Parameters
    __________
    identifier : list[str]
        The list of identifiers to be validated.

    Raises
    ______
    ValidationError
        If at least one of the identifiers is not a valid Ensemble identifier.
    """
    for value in values:
        if not is_null(value):
            validate_ensembl_identifier(value)


def validate_refseq_list(values: list[str]):
    """
    Validates whether each identifier in a list of identifiers (values) is a valid RefSeq identifier.

    Parameters
    __________
    identifier : list[str]
        The list of identifiers to be validated.

    Raises
    ______
    ValidationError
        If at least one of the identifiers is not a valid RefSeq identifier.
    """
    for value in values:
        if not is_null(value):
            validate_refseq_identifier(value)


def validate_uniprot_list(values: list[str]):
    """
    Validates whether each identifer in a list of identifiers (values) is a valid UniProt identifier.

    Parameters
    __________
    identifier : list[str]
        The list of identifiers to be validated.

    Raises
    ______
    ValidationError
        If at least one of the identifiers is not a valid UniProt identifier.
    """
    for value in values:
        if not is_null(value):
            validate_uniprot_identifier(value)
