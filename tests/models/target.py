from unittest import TestCase
from pydantic import ValidationError
from mavecore.models.target import TargetGene


class TestTargetGene(TestCase):
    def setUp(self):
        reference_map = {"genomeId": 0, "targetId": 0}
        sequence = {"sequenceType": "Protein", "sequence": "ATCGAA"}
        external_identifier_id = {"dbname": "UniProt", "identifier": "P01133"}
        external_identifier = {"identifier": external_identifier_id, "offset": 0}
        self.target = {"name": "name",
                       "category": "Protein coding",
                       "externalIdentifiers": [external_identifier],
                       "referenceMaps": [reference_map],
                       "wtSequence": sequence}

    def test_valid_all_fields(self):
        TargetGene.parse_obj(self.target)

    def test_invalid_category(self):
        self.target["category"] = "Protein"
        with self.assertRaises(ValidationError):
            TargetGene.parse_obj(self.target)

    def test_invalid_missing_required_field(self):
        self.target.pop("wtSequence")
        with self.assertRaises(ValidationError):
            TargetGene.parse_obj(self.target)
