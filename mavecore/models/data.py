from pydantic import BaseModel, ValidationError, validator
from typing import List, Dict, Optional

from .identifier import DoiIdentifier, PubmedIdentifier
from .target import TargetGene

from mavecore.validation.constants.urn import *
from mavecore.validation.utilities import is_null


class DataSet(BaseModel):
    title: str
    shortDescription: str
    abstractText: str
    methodText: str
    extraMetadata: Optional[Dict]
    keywords: Optional[List[str]]

    @validator('keywords')
    def validate_keywords(cls, v):
        if is_null(v):
            raise ValidationError("{} are not valid keywords. Keywords must be a valid list of strings.".format(v))
        else:
            for keyword in v:
                if is_null(keyword) or not isinstance(keyword, str):
                    raise ValidationError("{} not a valid keyword. Keywords must be valid strings.".format(keyword))


class Experiment(DataSet):
    doiIdentifiers: Optional[List[DoiIdentifier]]
    pubmedIdentifiers: Optional[List[PubmedIdentifier]]

    @validator('urn')
    def validate_urn_matches_regex(cls, v):
        regex = MAVEDB_TMP_URN_RE
        if not (re.fullmatch(regex, v)):
            raise ValidationError("{}'s is not a valid Experiment Set urn.".format(v))
        #if not (MAVEDB_EXPERIMENTSET_URN_RE.match(v) or MAVEDB_TMP_URN_RE.match(v)):
        #    raise ValidationError("{}'s is not a valid Experiment Set urn.".format(v))

    @validator('keywords')
    def validate_keywords(cls, v):
        if is_null(v):
            raise ValidationError("{} are not valid keywords. Keywords must be a valid list of strings.".format(v))
        else:
            for keyword in v:
                if is_null(keyword) or not isinstance(keyword, str):
                    raise ValidationError("{} not a valid keyword. Keywords must be valid strings.".format(keyword))

    @validator('experimentSetUrn')
    def validate_experiment_set_urn_matches_regex(cls, v):
        if not (MAVEDB_EXPERIMENT_URN_RE.match(v) or MAVEDB_TMP_URN_RE.match(v)):
            raise ValidationError("{}'s is not a valid Experiment urn.".format(v))


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
