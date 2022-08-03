from exceptions import ValidationError
import urn, summary, metadata, general, experiment


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
    if type(scoreset) != dict: raise ValidationError("The scoreset must be a dictionary.")
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
    #"extraMetadata": {},
    metadata.validate_metadata(scoreset.get("extraMetadata"))
    #"dataUsagePolicy": "string",
    #"licenceId": 0,
    #"replacesId": 0,
  "keywords": [
    "string"
  ],
  "numVariants": 0,
  "experiment": {
    "title": "string",
    "shortDescription": "string",
    "abstractText": "string",
    "methodText": "string",
    "extraMetadata": {},
    "keywords": [
      "string"
    ],
    "urn": "string",
    "numScoresets": 0,
    "createdBy": {
      "orcid_id": "string",
      "firstName": "string",
      "lastName": "string",
      "email": "string"
    },
    "modifiedBy": {
      "orcid_id": "string",
      "firstName": "string",
      "lastName": "string",
      "email": "string"
    },
    "creationDate": "2022-08-02",
    "modificationDate": "2022-08-02",
    "publishedDate": "2022-08-02",
    "experimentSetUrn": "string",
    "doiIdentifiers": [
      {
        "identifier": "string",
        "id": 0,
        "url": "string"
      }
    ],
    "pubmedIdentifiers": [
      {
        "identifier": "string",
        "id": 0,
        "url": "string",
        "referenceHtml": "string"
      }
    ],
    "processingState": "string"
  },
  "doiIdentifiers": [
    {
      "identifier": "string",
      "id": 0,
      "url": "string"
    }
  ],
  "pubmedIdentifiers": [
    {
      "identifier": "string",
      "id": 0,
      "url": "string",
      "referenceHtml": "string"
    }
  ],
  "publishedDate": "2022-08-02",
  "creationDate": "2022-08-02",
  "modificationDate": "2022-08-02",
  "createdBy": {
    "orcid_id": "string",
    "firstName": "string",
    "lastName": "string",
    "email": "string"
  },
  "modifiedBy": {
    "orcid_id": "string",
    "firstName": "string",
    "lastName": "string",
    "email": "string"
  },
  "targetGene": {
    "name": "string",
    "category": "string",
    "referenceMaps": [
      {
        "id": 0,
        "genomeId": 0,
        "targetId": 0,
        "isPrimary": true,
        "genome": {
          "shortName": "string",
          "organismName": "string",
          "genomeId": 0,
          "creationDate": "2022-08-02",
          "modificationDate": "2022-08-02",
          "id": 0
        },
        "creationDate": "2022-08-02",
        "modificationDate": "2022-08-02"
      }
    ],
    "wtSequence": {
      "sequenceType": "string",
      "sequence": "string"
    }
  },
  "datasetColumns": {},
  "private": true
}