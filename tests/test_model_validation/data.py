from unittest import TestCase
from pydantic import ValidationError
from mavecore.models.data import DataSet, Experiment, ExperimentSet, ScoreSet


class TestDataSet(TestCase):
    def test_valid_all_fields(self):
        user = {"orcid_id": "id", "firstName": "first", "lastName": "last", "email": "firstlast@email.edu"}
        dataset = {
            "title": "title",
            "shortDescription": "short description",
            "abstractText": "abstract",
            "methodText": "methods",
            "extraMetadata": {},
            "creationDate": "2022-02-02",
            "publishedDate": "2022-02-02",
            "modificationDate": "2022-02-02",
            "createdBy": user,
            "modifiedBy": user,
        }
        DataSet.parse_obj(dataset)

    def test_valid_exclude_optional(self):
        dataset = {
            "title": "title",
            "shortDescription": "short description",
            "abstractText": "abstract",
            "methodText": "methods",
        }
        DataSet.parse_obj(dataset)

    def test_invalid_creation_date(self):
        dataset = {
            "title": "title",
            "shortDescription": "short description",
            "abstractText": "abstract",
            "methodText": "methods",
            "creationDate": "2022-02-02-",
        }
        with self.assertRaises(ValidationError):
            DataSet.parse_obj(dataset)

    def test_invalid_published_date(self):
        dataset = {
            "title": "title",
            "shortDescription": "short description",
            "abstractText": "abstract",
            "methodText": "methods",
            "publishedDate": "2022-02-02-",
        }
        with self.assertRaises(ValidationError):
            DataSet.parse_obj(dataset)

    def test_invalid_modification_date(self):
        dataset = {
            "title": "title",
            "shortDescription": "short description",
            "abstractText": "abstract",
            "methodText": "methods",
            "creationDate": "2022-02-02",
            "publishedDate": "2022-02-02",
            "modificationDate": "a",
        }
        with self.assertRaises(ValidationError):
            DataSet.parse_obj(dataset)


class TestExperiment(TestCase):
    def test_valid_all_fields(self):
        user = {"orcid_id": "id", "firstName": "first", "lastName": "last", "email": "firstlast@email.edu"}
        doi_identifier = {"identifier": "id"}
        pubmed_identifier = {"identifier": "id"}
        experiment = {
            "title": "title",
            "shortDescription": "short description",
            "abstractText": "abstract",
            "methodText": "methods",
            "extraMetadata": {},
            "creationDate": "2022-02-02",
            "publishedDate": "2022-02-02",
            "modificationDate": "2022-02-02",
            "createdBy": user,
            "modifiedBy": user,
            "urn": "tmp:070b3886-ed72-4ce9-a574-6754ad00310b",
            "keywords": ["string"],
            "numScoresets": 0,
            #"experimentSetUrn": "urn",
            "doiIdentifiers": [doi_identifier],
            "pubmedIdentifiers": [pubmed_identifier],
            "processingState": "string",
        }
        DataSet.parse_obj(dictionary)
