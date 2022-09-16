from pydantic import BaseModel, ValidationError, validator
from typing import List, Dict, Optional

from .identifier import DoiIdentifier, PubmedIdentifier
from .target import TargetGene

from mavecore.validation.constants.urn import *
from mavecore.validation.utilities import is_null
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
    urn: Optional[str]
    dataUsagePolicy: str
    licenceId: int
    replacesId: Optional[int]
    experimentUrn: str
    doiIdentifiers: Optional[List[DoiIdentifier]]
    pubmedIdentifiers: Optional[List[PubmedIdentifier]]
    targetGene: TargetGene

    @validator('urn')
    def validate_matches_regular_expression(cls, v):
        if not (MAVEDB_SCORESET_URN_RE.match(v) or MAVEDB_TMP_URN_RE.match(v)):
            raise ValidationError("{}'s is not a valid score set urn.".format(v))
