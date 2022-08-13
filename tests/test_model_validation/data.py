from unittest import TestCase
from pydantic import ValidationError
from mavecore.models.data import DataSet, Experiment, ExperimentSet, ScoreSet



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
