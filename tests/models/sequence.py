from unittest import TestCase
from pydantic import ValidationError
from mavecore.models.sequence import WildType


class Test(TestCase):
    def test_valid_all_fields(self):
        sequence = {
            "sequence_type": "Protein",
            "sequence": "ATC",
        }
        WildType.parse_obj(sequence)

    def test_invalid_sequence_type(self):
        sequence = {
            "sequence_type": "RNA",
            "sequence": "ATC",
        }
        with self.assertRaises(ValidationError):
            WildType.parse_obj(sequence)
