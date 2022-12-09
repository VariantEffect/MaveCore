from unittest import TestCase
from mavecore.validation.dataset import validate_experiment, validate_scoreset


class TestValidateExperiment(TestCase):
    def setUp(self):
        doi_identifier = {"identifier": "10.1038/s41588-018-0122-z"}
        pubmed_identifier = {"identifier": "29785012"}
        self.experiment = {
            "title": "title",
            "short_description": "short description",
            "abstract_text": "abstract",
            "method_text": "methods",
            "extra_metadata": {},
            "keywords": ["string"],
            "doi_identifiers": [doi_identifier],
            "pubmed_identifiers": [pubmed_identifier],
        }

    def test_valid_all_fields(self):
        validate_experiment(self.experiment)
        '''try:
            print(type(json.loads(Experiment.parse_obj(self.experiment).json())))
            #print(a.json())

            #b = dict()
            #print(b.json())
        except ValueError as e:
            print(e)'''

    def test_valid_exclude_optional(self):
        self.experiment.pop("extra_metadata")
        self.experiment.pop("keywords")
        self.experiment.pop("doi_identifiers")
        self.experiment.pop("pubmed_identifiers")
        validate_experiment(self.experiment)


class TestValidateScoreSet(TestCase):
    def setUp(self):
        doi_identifier = {"identifier": "10.1038/s41588-018-0122-z"}
        pubmed_identifier = {"identifier": "29785012"}
        reference_map = {"genome_id": 0, "target_id": 0}
        sequence = {"sequence_type": "DNA", "sequence": "ATC"}
        external_identifier_id = {"dbname": "UniProt", "identifier": "P01133"}
        external_identifier = {"identifier": external_identifier_id, "offset": 0}
        target = {"name": "name",
                  "category": "Protein coding",
                  "external_identifiers": [external_identifier],
                  "reference_maps": [reference_map],
                  "wt_sequence": sequence}
        self.scoreset = {
            "title": "title",
            "short_description": "short description",
            "abstract_text": "abstract",
            "method_text": "methods",
            "extra_metadata": {},
            "data_usage_policy": "policy",
            "licence_id": 0,
            "keywords": ["string"],
            "experiment_urn": "tmp:0a56b8eb-8e19-4906-8cc7-d17d884330a5",
            "superseded_scoreset_urn": "tmp:0a56b8eb-8e19-4906-8cc7-d17d884330a5",
            "meta_analysis_source_scoreset_urns": ["tmp:0a56b8eb-8e19-4906-8cc7-d17d884330a5"],
            "doi_identifiers": [doi_identifier],
            "pubmed_identifiers": [pubmed_identifier],
            "target_gene": target,
        }

    def test_valid_all_fields(self):
        validate_scoreset(self.scoreset)

    def test_valid_exclude_optional(self):
        self.scoreset.pop("extra_metadata")
        self.scoreset.pop("keywords")
        self.scoreset.pop("doi_identifiers")
        self.scoreset.pop("pubmed_identifiers")
        self.scoreset.pop("superseded_scoreset_urn")
        self.scoreset.pop("meta_analysis_source_scoreset_urns")
        validate_scoreset(self.scoreset)
