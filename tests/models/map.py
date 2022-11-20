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
