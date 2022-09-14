from unittest import TestCase
from pydantic import ValidationError
from mavecore.models.sequence import WildType


class Test(TestCase):
    def test_valid_all_fields(self):
        sequence = {
            "sequenceType": "Protein",
            "sequence": "ATCG",
        }
        WildType.parse_obj(sequence)

    def test_invalid_sequence_type(self):
        sequence = {
            "sequenceType": "RNA",
            "sequence": "ATCG",
        }
        with self.assertRaises(ValidationError):
            WildType.parse_obj(sequence)
