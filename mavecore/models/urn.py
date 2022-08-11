from pydantic import BaseModel, ValidationError, validator

from ..validation_new.constants.urn import *
from ..validation_new.exceptions import ValidationError


class Urn(BaseModel):
    urn: str

    @validator('urn')
    def must_match_regular_expression(cls, v):
        if not MAVEDB_ANY_URN_RE.match(v):
            raise ValueError("{}'s is not a valid urn.".format(v))
