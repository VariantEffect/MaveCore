from pydantic import BaseModel, ValidationError, validator

from ..validation_new.constants.urn import *
from ..validation_new.exceptions import ValidationError


class Urn(BaseModel):
    urn: str


class ExperimentUrn(Urn):
    @validator('urn')
    def must_match_regular_expression(cls, v):
        if not (MAVEDB_EXPERIMENTSET_URN_RE.match(v) or MAVEDB_TMP_URN_RE.match(v)):
            raise ValidationError("{}'s is not a valid Experiment Set urn.".format(v))


class ExperimentSetUrn(Urn):
    @validator('urn')
    def must_match_regular_expression(cls, v):
        if not (MAVEDB_EXPERIMENT_URN_RE.match(v) or MAVEDB_TMP_URN_RE.match(v)):
            raise ValidationError("{}'s is not a valid Experiment urn.".format(v))


class ScoreSetUrn(Urn):
    @validator('urn')
    def must_match_regular_expression(cls, v):
        if not (MAVEDB_SCORESET_URN_RE.match(v) or MAVEDB_TMP_URN_RE.match(v)):
            raise ValidationError("{}'s is not a valid score set urn.".format(v))