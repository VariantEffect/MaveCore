from pydantic import BaseModel, validator
from typing import List, Dict, Optional

from .identifier import DoiIdentifier, PubmedIdentifier
from .target import TargetGene

from mavecore.validation import keywords, urn


class DataSet(BaseModel):
    title: str
    shortDescription: str
    abstractText: str
    methodText: str
    extraMetadata: Optional[Dict]
    keywords: Optional[List[str]]

    @validator('keywords')
    def validate_keywords(cls, v):
        keywords.validate_keywords(v)


class Experiment(DataSet):
    doiIdentifiers: Optional[List[DoiIdentifier]]
    pubmedIdentifiers: Optional[List[PubmedIdentifier]]


class ScoreSet(DataSet):
    dataUsagePolicy: str
    licenceId: int
    experimentUrn: str
    supersededScoresetUrn: Optional[str]
    metaAnalysisSourceScoresetUrns: Optional[List[str]]
    doiIdentifiers: Optional[List[DoiIdentifier]]
    pubmedIdentifiers: Optional[List[PubmedIdentifier]]
    targetGene: TargetGene

    @validator('experimentUrn', 'supersededScoresetUrn')
    def validate_matches_regular_expression(cls, v):
        urn.validate_mavedb_urn_scoreset(v)
