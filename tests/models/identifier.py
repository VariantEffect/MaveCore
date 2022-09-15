from unittest import TestCase
from pydantic import ValidationError
from mavecore.models.identifier import Identifier, DoiIdentifier, PubmedIdentifier


class TestIdentifier(TestCase):
    def setUp(self):
        self.identifier = {
            "identifier": "10.1038/s41588-018-0122-z",
            "id": 0,
            "url": "https://www.uw.edu",
        }

    def test_valid_all_fields(self):
        Identifier.parse_obj(self.identifier)

    def test_valid_exclude_optional(self):
        self.identifier.pop("id")
        self.identifier.pop("url")
        Identifier.parse_obj(self.identifier)

    def test_invalid_url(self):
        self.identifier["url"] = "www.uw.edu"
        with self.assertRaises(ValidationError):
            Identifier.parse_obj(self.identifier)


class TestDoiIdentifier(TestCase):
    def setUp(self):
        self.doi_identifier = {
            "identifier": "10.1038/s41588-018-0122-z",
            "id": 0,
            "url": "https://www.uw.edu",
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
            "id": 0,
            "url": "https://www.uw.edu",
            "referenceHtml": "referencehtml",
        }

    def test_valid_all_fields(self):
        PubmedIdentifier.parse_obj(self.pubmed_identifier)

    def test_valid_exclude_optional(self):
        self.pubmed_identifier.pop("id")
        self.pubmed_identifier.pop("url")
        self.pubmed_identifier.pop("referenceHtml")
        PubmedIdentifier.parse_obj(self.pubmed_identifier)

    def test_invalid_type_of_identifier(self):
        self.pubmed_identifier["identifier"] = "10.1038/s41588-018-0122-z"
        with self.assertRaises(ValidationError):
            PubmedIdentifier.parse_obj(self.pubmed_identifier)
