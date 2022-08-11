from unittest import TestCase
from pydantic import BaseModel
from mavecore.models.data import DataSet # data#, genome, identifier, map, sequence, target, urn, user


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
