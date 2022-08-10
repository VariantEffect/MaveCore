from pydantic import BaseModel

class DataSet(BaseModel):

class ExperimentSet(DataSet):

class Experiment(DataSet):

class ScoreSet(DataSet):