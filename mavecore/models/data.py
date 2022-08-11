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
    extraMetadata: dict
    creationDate: datetime
    publishedDate: datetime
    modificationDate: datetime
    createdBy: User
    modifiedBy: User


class Experiment(DataSet):
    urn: ExperimentUrn
    keywords: List[str]
    numScoresets: int
    experimentSetUrn: Urn
    doiIdentifiers: DoiIdentifier
    pubmedIdentifiers: PubmedIdentifier
    processingState: str


class ExperimentSet(DataSet):
    urn: ExperimentSetUrn
    id: int
    experiments: list[Experiment]
    numExperiments: int


class ScoreSet(DataSet):
    urn: ScoreSetUrn
    dataUsagePolicy: str
    licenceId: int
    replacesId: int
    keywords: list[str]
    numVariants: int
    experiment: Experiment
    doiIdentifiers: DoiIdentifier
    pubmedIdentifiers: PubmedIdentifier
    targetGene: TargetGene
    datasetColumns: dict
    private: bool
