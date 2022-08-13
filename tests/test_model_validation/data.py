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

class Test(TestCase):
    def test_no_change(self):
        """
        class DataSet(BaseModel):
            title: str
            shortDescription: str
            abstractText: str
            methodText: str"""

        dictionary ={
          "title": "string",
          "shortDescription": "string",
          "abstractText": "string",
          "methodText": "string",
        }
        DataSet.parse_obj(dictionary)
