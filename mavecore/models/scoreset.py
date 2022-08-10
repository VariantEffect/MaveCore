from dataset import DataSet

class ScoreSet(DataSet):
    urn: str
    title: str
    methodText: str
    abstractText: str
    shortDescription: str
    extraMetadata: dict
    dataUsagePolicy: str
    licenceId: int
    replacesId: int
    keywords: list[str]
    numVariants: int
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
        "creationDate": "2022-08-10",
        "modificationDate": "2022-08-10",
        "publishedDate": "2022-08-10",
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
    "publishedDate": "2022-08-10",
    "creationDate": "2022-08-10",
    "modificationDate": "2022-08-10",
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
                    "creationDate": "2022-08-10",
                    "modificationDate": "2022-08-10",
                    "id": 0
                },
                "creationDate": "2022-08-10",
                "modificationDate": "2022-08-10"
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