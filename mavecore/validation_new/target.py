from exceptions import ValidationError
from type import *


def validate_target_gene(targetGene):
    """
    Validates target gene represented as a dictionary.

    Parameters:
    __________
    targetGene: dict
        The target gene to be validated

    Raises:
    ______
    ValidationError
        If the target gene is not represented as a dictionary or if any of the key value pairs are invalid.
    """
    is_dictionary(targetGene)
    #  "targetGene": {
    #    "name": "string",
    #    "category": "string",
    #    "referenceMaps": [
    #    ],
    #    "wtSequence": {
    #      "sequenceType": "string",
    #      "sequence": "string"
    #    }
    #  },


def validate_name(name):
    is_string(name)


def validate_category(category):
    is_string(category)


def validate_reference_maps(referenceMaps):
    """
    Validates reference maps for the target gene.

    Parameters:
    __________
    referenceMaps: list[dict]
        The list of reference maps to be validated

    Raises:
    ______
    ValidationError
        If the referenceMaps are not a list of dictionaries
        or if any of the key value pairs in the dictionary are invalid
    """
    is_list(referenceMaps)
    is_integer(referenceMaps.get("id"))
    is_integer(referenceMaps.get("genomeId"))

# {
#        "id": 0,
#        "genomeId": 0,
#        "targetId": 0,
#        "isPrimary": true,
#        "genome": {
#          "shortName": "string",
#          "organismName": "string",
#          "genomeId": 0,
#          "creationDate": "2022-08-02",
#          "modificationDate": "2022-08-02",
#          "id": 0
#        },
#        "creationDate": "2022-08-02",
#        "modificationDate": "2022-08-02"
#      }


def validate_wt_sequence(wtSequence):
    return