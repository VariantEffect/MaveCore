from unittest import TestCase
from pydantic import ValidationError
from mavecore.models.identifier import (Identifier,
                                        DoiIdentifier,
                                        PubmedIdentifier,
                                        #ExternalIdentifierId,
                                        ExternalIdentifier)


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


class TestExternalIdentifier(TestCase):
    def setUp(self):
        self.external_identifier_id = {"dbname": "UniProt", "identifier": "P01133"}
        self.external_identifier = {"identifier": self.external_identifier_id, "offset": 0}

    """def test_valid_external_identifier_id(self):
        print(hasattr(self.external_identifier_id, "dbname"))
        ExternalIdentifierId.parse_obj(self.external_identifier_id)"""

    def test_valid_external_identifier(self):
        ExternalIdentifier.parse_obj(self.external_identifier)