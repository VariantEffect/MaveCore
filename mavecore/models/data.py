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
    urn: Optional[str]
    keywords: Optional[List[str]]
    numScoresets: Optional[int]
    experimentSetUrn: Optional[str]
    doiIdentifiers: Optional[List[DoiIdentifier]]
    pubmedIdentifiers: Optional[List[PubmedIdentifier]]
    processingState: Optional[str]

    @validator('urn')
    def urn_must_match_regex(cls, v):
        regex = MAVEDB_TMP_URN_RE
        if not (re.fullmatch(regex, v)):
            raise ValidationError("{}'s is not a valid Experiment Set urn.".format(v))
        #if not (MAVEDB_EXPERIMENTSET_URN_RE.match(v) or MAVEDB_TMP_URN_RE.match(v)):
        #    raise ValidationError("{}'s is not a valid Experiment Set urn.".format(v))

    @validator('experimentSetUrn')
    def experiment_set_urn_must_match_regex(cls, v):
        if not (MAVEDB_EXPERIMENT_URN_RE.match(v) or MAVEDB_TMP_URN_RE.match(v)):
            raise ValidationError("{}'s is not a valid Experiment urn.".format(v))


class ExperimentSet(DataSet):
    urn: Optional[str]
    id: int
    experiments: List[Experiment]
    numExperiments: int

    @validator('urn')
    def must_match_regular_expression(cls, v):
        if not (MAVEDB_EXPERIMENT_URN_RE.match(v) or MAVEDB_TMP_URN_RE.match(v)):
            raise ValidationError("{}'s is not a valid Experiment urn.".format(v))


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
