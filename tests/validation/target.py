from unittest import TestCase

from mavecore.validation.target import *
from mavecore.validation.exceptions import ValidationError
from mavecore.validation.constants.target import valid_categories, valid_sequence_types


class TestValidateTargetCategory(TestCase):
    def test_valid(self):
        for category in valid_categories:
            validate_target_category(category)


class TestValidateSequenceCategory(TestCase):
    def test_valid(self):
        for sequence_type in valid_sequence_types:
            validate_sequence_category(sequence_type)


class TestValidateTargetSequence(TestCase):
    def setUp(self):
        self.target_seq = "ATGACCAAACAT"

    def test_valid(self):
        validate_target_sequence(self.target_seq)
