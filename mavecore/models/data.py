from pydantic import BaseModel
from datetime import datetime

from user import User
from urn import Urn
from identifier import *
from target import Target


class DataSet(BaseModel):

class ExperimentSet(DataSet):

class Experiment(DataSet):

class ScoreSet(DataSet):