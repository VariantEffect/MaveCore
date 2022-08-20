from unittest import TestCase
from mavecore.models.identifier import Identifier, DoiIdentifier, PubmedIdentifier


class TestIdentifier(TestCase):
    def test_valid_all_fields(self):
        identifier = {
            "identifier": "10.1038/s41588-018-0122-z",
            "id": 0,
            "url": "https://www.uw.edu",
        }
        Identifier.parse_obj(identifier)

    def test_valid_exclude_optional(self):
        identifier = {
            "identifier": "29785012",
        }
        Identifier.parse_obj(identifier)

    def test_invalid_url(self):
        identifier = {
            "identifier": "29785012",
            "id": 0,
            "url": "www.uw.edu",
        }
        with self.assertRaises(ValueError):
            Identifier.parse_obj(identifier)


class TestDoiIdentifier(TestCase):
    def test_valid_all_fields(self):
        doi_identifier = {
            "identifier": "10.1038/s41588-018-0122-z",
            "id": 0,
            "url": "https://www.uw.edu",
        }
        DoiIdentifier.parse_obj(doi_identifier)


class TestPubmedIdentifier(TestCase):
    def test_valid_all_fields(self):
        pubmed_identifier = {
            "identifier": "29785012",
            "id": 0,
            "url": "https://www.uw.edu",
            "referenceHtml": "referencehtml",
        }
        PubmedIdentifier.parse_obj(pubmed_identifier)

    def test_valid_exclude_optional(self):
        pubmed_identifier = {
            "identifier": "id",
        }
        PubmedIdentifier.parse_obj(pubmed_identifier)
