from type import *
import summary, metadata, urn, user, general, identifiers


def validate_experiment(experiment):
    """
    This function validates an experiment.

    Parameters:
    __________
    experiment: dict
        The experiment represented as a dictionary.

    Raises:
    ______
    ValidationError
        If the experiment is not a dictionary or if any key:value pair in the experiment is not valid.
    """
    # check type
    is_dictionary(experiment)
    #  "experiment": {
    #    "title": "string",
    #    "shortDescription": "string",
    #    "abstractText": "string",
    #    "methodText": "string",
    summary.validate_title(experiment.get("title"))
    summary.validate_short_description(experiment.get("shortDescription"))
    summary.validate_abstract(experiment.get("abstractText"))
    summary.validate_methods(experiment.get("methodText"))
    #    "extraMetadata": {},
    metadata.validate_metadata(experiment.get("extraMetadata"))
    #    "keywords": [
    #      "string"
    #    ],
    summary.validate_keywords(experiment.get("keywords"))
    #    "urn": "string",
    urn.validate_experiment_urn(experiment.get("urn"))
    #    "numScoresets": 0,
    summary.validate_num_scoresets(experiment.get("numScoresets"))
    #    "createdBy": {
    #      "orcid_id": "string",
    #      "firstName": "string",
    #      "lastName": "string",
    #      "email": "string"
    #    },
    #    "modifiedBy": {
    #      "orcid_id": "string",
    #      "firstName": "string",
    #      "lastName": "string",
    #      "email": "string"
    #    },
    #    "creationDate": "2022-08-02",
    #    "modificationDate": "2022-08-02",
    #    "publishedDate": "2022-08-02",
    #    "experimentSetUrn": "string",
    #    "doiIdentifiers": [
    #      {
    #        "identifier": "string",
    #        "id": 0,
    #        "url": "string"
    #      }
    #    ],
    #    "pubmedIdentifiers": [
    #      {
    #        "identifier": "string",
    #        "id": 0,
    #        "url": "string",
    #        "referenceHtml": "string"
    #      }
    #    ],
    #    "processingState": "string"
    #  },