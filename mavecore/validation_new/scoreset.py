from exceptions import ValidationError
from type import *
import urn, summary, metadata, general, experiment, identifiers, user, target


def validate_scoreset(scoreset, files):
    """
    Validates a scoreset represented as a dictionary.

    Parameters:
    __________
    scoreset: Dict
        The scoreset that will be validated.
    files: path
        The path to the files belonging to the scoreset.

    Raises:
    ______
    ValidationError
        If scoreset is not a dictionary or if any additional validation fails.
    """
    # first validate that scoreset is a dictionary
    is_dictionary(scoreset)
    # {
    #  "urn": "string",
    #  "title": "string",
    #  "methodText": "string",
    #  "abstractText": "string",
    #  "shortDescription": "string",
    urn.validate_scoreset_urn(scoreset.get("urn"))
    summary.validate_title(scoreset.get("title"))
    summary.validate_methods(scoreset.get("methodText"))
    summary.validate_abstract(scoreset.get("abstractText"))
    summary.validate_short_description(scoreset.get("shortDescription"))
    #  "extraMetadata": {},
    metadata.validate_metadata(scoreset.get("extraMetadata"))
    #  "dataUsagePolicy": "string",
    #  "licenceId": 0,
    #  "replacesId": 0,
    general.validate_data_usage_policy(scoreset.get("dataUsagePolicy"))
    general.validate_license_id(scoreset.get("licenseId"))
    general.validate_replaces_id(scoreset.get("replacesId"))
    #  "keywords": [
    #    "string"
    #  ],
    summary.validate_keywords(scoreset.get("keywords"))
    #  "numVariants": 0,
    summary.validate_num_variants(scoreset.get("numVariants"))
    #  "experiment": {
    #  },
    experiment.validate_experiemnt(scoreset.get("experiment"))
    #  "doiIdentifiers": [
    #    {
    #    }
    #  ],
    #  "pubmedIdentifiers": [
    #    {
    #    }
    #  ],
    identifiers.validate_doi_identifiers(scoreset.get("doiIdentifiers"))
    identifiers.validate_pubmed_identifiers(scoreset.get("pubmedIdentifiers"))
    #  "publishedDate": "2022-08-02",
    #  "creationDate": "2022-08-02",
    #  "modificationDate": "2022-08-02",
    general.validate_date(scoreset.get("publishedDate"))
    general.validate_date(scoreset.get("creationDate"))
    general.validate_date(scoreset.get("modificationDate"))
    #  "createdBy": {
    #    "orcid_id": "string",
    #    "firstName": "string",
    #    "lastName": "string",
    #    "email": "string"
    #  },
    #  "modifiedBy": {
    #    "orcid_id": "string",
    #    "firstName": "string",
    #    "lastName": "string",
    #    "email": "string"
    #  },
    user.validate_user(scoreset.get("createdBy"))
    user.validate_user(scoreset.get("modifiedBy"))
    #  "targetGene": {
    #  },
    target.validate_target_gene(scoreset.get("targetGene"))
    #  "datasetColumns": {},
    summary.validate_dataset_columns(scoreset.get("datasetColumns"))
    #  "private": true
    general.validate_private(scoreset.get("private"))
    # }
