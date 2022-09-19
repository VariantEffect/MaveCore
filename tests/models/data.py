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
        external_identifier_id = {"dbname": "str", "identifier": "str"}
        external_identifier = {"identifier": external_identifier_id, "offset": 0}
        target = {"name": "name",
                  "category": "Protein coding",
                  "externalIdentifiers": [external_identifier],
                  "referenceMaps": [reference_map],
                  "wtSequence": sequence}
        self.scoreset = {
            "title": "title",
            "shortDescription": "short description",
            "abstractText": "abstract",
            "methodText": "methods",
            "extraMetadata": {},
            "dataUsagePolicy": "policy",
            "licenceId": 0,
            "keywords": ["string"],
            "experimentUrn": "tmp:0a56b8eb-8e19-4906-8cc7-d17d884330a5",
            "supersededScoresetUrn": "tmp:0a56b8eb-8e19-4906-8cc7-d17d884330a5",
            "metaAnalysisSourceScoresetUrns": ["tmp:0a56b8eb-8e19-4906-8cc7-d17d884330a5"],
            "doiIdentifiers": [doi_identifier],
            "pubmedIdentifiers": [pubmed_identifier],
            "targetGene": target,
        }

    def test_valid_all_fields(self):
        ScoreSet.parse_obj(self.scoreset)

    def test_valid_exclude_optional(self):
        self.scoreset.pop("extraMetadata")
        self.scoreset.pop("keywords")
        self.scoreset.pop("doiIdentifiers")
        self.scoreset.pop("pubmedIdentifiers")
        self.scoreset.pop("supersededScoresetUrn")
        self.scoreset.pop("metaAnalysisSourceScoresetUrns")
        ScoreSet.parse_obj(self.scoreset)

