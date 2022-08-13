from pydantic import BaseModel, ValidationError, validator
from datetime import datetime
from typing import List, Dict, Optional

from .user import User
from .identifier import DoiIdentifier, PubmedIdentifier
from .target import TargetGene

from mavecore.validation_new.constants.urn import *


class DataSet(BaseModel):
    title: str
    shortDescription: str
    abstractText: str
    methodText: str
    extraMetadata: Optional[Dict]
    creationDate: Optional[str]
    publishedDate: Optional[str]
    modificationDate: Optional[str]
    createdBy: Optional[User]
    modifiedBy: Optional[User]

    @validator('creationDate', 'publishedDate', 'modificationDate')
    def date_must_match_regex(cls, v):
        # regular expression for validating a date
        regex = '%Y-%m-%d'
        if not bool(datetime.strptime(v, regex)):
            raise ValidationError("{}'s is not a valid date.".format(v))


class Experiment(DataSet):
    urn: ExperimentUrn
    keywords: List[str]
    numScoresets: int
    experimentSetUrn: ExperimentSetUrn
    doiIdentifiers: Optional[DoiIdentifier]
    pubmedIdentifiers: Optional[PubmedIdentifier]
    processingState: str


class ExperimentSet(DataSet):
    urn: ExperimentSetUrn
    id: int
    experiments: List[Experiment]
    numExperiments: int


class ScoreSet(DataSet):
    urn: ScoreSetUrn
    dataUsagePolicy: str
    licenceId: int
    replacesId: Optional[int]
    keywords: Optional[List[str]]
    numVariants: int
    experiment: Experiment
    doiIdentifiers: Optional[DoiIdentifier]
    pubmedIdentifiers: Optional[PubmedIdentifier]
    targetGene: TargetGene
    datasetColumns: Dict
    private: bool
