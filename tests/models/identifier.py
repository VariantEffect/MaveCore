from unittest import TestCase
from pydantic import ValidationError
from mavecore.models.identifier import Identifier, DoiIdentifier, PubmedIdentifier


class TestIdentifier(TestCase):
    def setUp(self):
        self.identifier = {
            "identifier": "10.1038/s41588-018-0122-z",
        }

    def test_valid_all_fields(self):
        Identifier.parse_obj(self.identifier)


class TestDoiIdentifier(TestCase):
    def setUp(self):
        self.doi_identifier = {
            "identifier": "10.1038/s41588-018-0122-z",
        }

    def test_valid_all_fields(self):
        DoiIdentifier.parse_obj(self.doi_identifier)

    def test_invalid_type_of_identifier(self):
        self.doi_identifier["identifier"] = "29785012"
        with self.assertRaises(ValidationError):
            DoiIdentifier.parse_obj(self.doi_identifier)


class TestPubmedIdentifier(TestCase):
    def setUp(self):
        self.pubmed_identifier = {
            "identifier": "29785012",
        }

    def test_valid_all_fields(self):
        PubmedIdentifier.parse_obj(self.pubmed_identifier)

    def test_invalid_type_of_identifier(self):
        self.pubmed_identifier["identifier"] = "10.1038/s41588-018-0122-z"
        with self.assertRaises(ValidationError):
            PubmedIdentifier.parse_obj(self.pubmed_identifier)
