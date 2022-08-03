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
    #    "extraMetadata": {},
    #    "keywords": [
    #      "string"
    #    ],
    #    "urn": "string",
    #    "numScoresets": 0,
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