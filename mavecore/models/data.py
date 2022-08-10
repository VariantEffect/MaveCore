from pydantic import BaseModel
from datetime import datetime

from user import User
from urn import Urn
from identifier import *
from target import Target


class DataSet(BaseModel):
    urn: str
    title: str
    shortDescription: str
    abstractText: str
    methodText: str
    extraMetadata: dict
    creationDate: datetime
    publishedDate: datetime
    modificationDate: datetime
    createdBy: User
    modifiedBy: User

class ExperimentSet(DataSet):

class Experiment(DataSet):

class ScoreSet(DataSet):