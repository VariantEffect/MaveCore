from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Optional

from user import User
from identifier import DoiIdentifier, PubmedIdentifier
from target import TargetGene
from urn import ExperimentUrn, ExperimentSetUrn, ScoreSetUrn


class DataSet(BaseModel):
    title: str
    shortDescription: str
    abstractText: str
    methodText: str
    extraMetadata: Optional[Dict]
    creationDate: datetime
    publishedDate: Optional[datetime]
    modificationDate: Optional[datetime]
    createdBy: Optional[User]
    modifiedBy: Optional[User]


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
