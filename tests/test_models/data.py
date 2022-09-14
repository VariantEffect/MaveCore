from unittest import TestCase
from pydantic import ValidationError
from mavecore.models.data import DataSet, Experiment, ScoreSet


class TestDataSet(TestCase):
    def setUp(self):
        self.dataset = {
            "title": "title",
            "shortDescription": "short description",
            "abstractText": "abstract",
            "methodText": "methods",
            "extraMetadata": {},
            "keywords": ["string"],
        }

    def test_valid_all_fields(self):
        DataSet.parse_obj(self.dataset)

    def test_valid_exclude_optional(self):
        self.dataset.pop("extraMetadata")
        self.dataset.pop("keywords")
        DataSet.parse_obj(self.dataset)

    def test_invalid_keywords(self):
        self.dataset["keywords"] = ["null"]
        with self.assertRaises(ValidationError):
            Experiment.parse_obj(self.dataset)


class TestExperiment(TestCase):
    def setUp(self):
        doi_identifier = {"identifier": "10.1038/s41588-018-0122-z"}
        pubmed_identifier = {"identifier": "29785012"}
        self.experiment = {
            "title": "title",
            "shortDescription": "short description",
            "abstractText": "abstract",
            "methodText": "methods",
            "extraMetadata": {},
            "keywords": ["string"],
            "doiIdentifiers": [doi_identifier],
            "pubmedIdentifiers": [pubmed_identifier],
        }

    def test_valid_all_fields(self):
        Experiment.parse_obj(self.experiment)

    def test_valid_exclude_optional(self):
        self.experiment.pop("extraMetadata")
        self.experiment.pop("keywords")
        self.experiment.pop("doiIdentifiers")
        self.experiment.pop("pubmedIdentifiers")
        Experiment.parse_obj(self.experiment)


class TestScoreSet(TestCase):
    def setUp(self):
        doi_identifier = {"identifier": "10.1038/s41588-018-0122-z"}
        pubmed_identifier = {"identifier": "29785012"}
        reference_map = {"genomeId": 0, "targetId": 0}
        sequence = {"sequenceType": "DNA", "sequence": "ATCG"}
        target = {"name": "name",
                  "category": "Protein coding",
                  "ensembleIdId": 0,
                  "refseqIdId": 0,
                  "uniprotIdId": 0,
                  "referenceMaps": [reference_map],
                  "wtSequence": sequence}
        self.scoreset = {
            "title": "title",
            "shortDescription": "short description",
            "abstractText": "abstract",
            "methodText": "methods",
            "extraMetadata": {},
            # "urn": "urn",
            "dataUsagePolicy": "policy",
            "licenceId": 0,
            "replacesId": 0,
            "keywords": ["string"],
            "experimentUrn": "urn",
            "doiIdentifiers": [doi_identifier],
            "pubmedIdentifiers": [pubmed_identifier],
            "targetGene": target,
        }

    def test_valid_all_fields(self):
        ScoreSet.parse_obj(self.scoreset)

    def test_valid_exclude_optional(self):
        self.scoreset.pop("extraMetadata")
        self.scoreset.pop("keywords")
        self.scoreset.pop("replacesId")
        self.scoreset.pop("doiIdentifiers")
        self.scoreset.pop("pubmedIdentifiers")
        ScoreSet.parse_obj(self.scoreset)

