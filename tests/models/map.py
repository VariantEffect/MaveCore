from unittest import TestCase
from mavecore.models.map import ReferenceMap


class TestReferenceMap(TestCase):
    def setUp(self):
        self.reference_map = {
            "genomeId": 0,
            "targetId": 0,
        }

    def test_valid_all_fields(self):
        ReferenceMap.parse_obj(self.reference_map)

    def test_valid_exclude_optional(self):
        genome = {"shortName": "name", "organismName": "organism", "genomeId": 0, "id": 0}
        reference_map = {
            "id": 0,
            "genomeId": 0,
            "targetId": 0,
            "isPrimary": True,
            "genome": genome,
        }
        ReferenceMap.parse_obj(reference_map)

    def test_invalid_creation_date(self):
        genome = {"shortName": "name", "organismName": "organism", "genomeId": 0, "id": 0}
        reference_map = {
            "id": 0,
            "genomeId": 0,
            "targetId": 0,
            "isPrimary": True,
            "genome": genome,
            "creationDate": "2022-02-02-",
        }
        with self.assertRaises(ValidationError):
            ReferenceMap.parse_obj(reference_map)
