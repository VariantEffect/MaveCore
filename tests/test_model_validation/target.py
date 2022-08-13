from unittest import TestCase
from pydantic import ValidationError
from mavecore.models.target import TargetGene


class TestTargetGene(TestCase):
    def test_valid_all_fields(self):
        genome = {"shortName": "name", "organismName": "organism", "genomeId": 0, "id": 0}
        reference_map = {"id": 0, "genomeId": 0, "targetId": 0, "isPrimary": True, "genome": genome}
        sequence = {"sequenceType": "type", "sequence": "ATCG"}
        target = {
            "name": "name",
            "category": "Protein coding",
            "referenceMaps": [reference_map],
            "wtSequence": sequence,
        }
        TargetGene.parse_obj(target)

    def test_invalid_category(self):
        genome = {"shortName": "names", "organismName": "organism", "genomeId": 0, "id": 0}
        reference_map = {"id": 0, "genomeId": 0, "targetId": 0, "isPrimary": True, "genome": genome}
        sequence = {"sequenceType": "type", "sequence": "ATCG"}
        target = {
            "name": "name",
            "category": "Protein",
            "referenceMaps": [reference_map],
            "wtSequence": sequence,
        }
        with self.assertRaises(ValidationError):
            TargetGene.parse_obj(target)

    def test_invalid_missing_required_field(self):
        genome = {"shortName": "name", "organismName": "organism", "genomeId": 0, "id": 0}
        reference_map = {"id": 0, "genomeId": 0, "targetId": 0, "isPrimary": True, "genome": genome}
        target = {
            "name": "name",
            "category": "Protein coding",
            "referenceMaps": [reference_map],
        }
        with self.assertRaises(ValidationError):
            TargetGene.parse_obj(target)
