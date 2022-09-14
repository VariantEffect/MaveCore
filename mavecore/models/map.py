from pydantic import BaseModel, ValidationError, validator
from datetime import datetime
from typing import Optional


class ReferenceMap(BaseModel):
    genomeId: int
    targetId: int

    @validator('creationDate', 'modificationDate')
    def date_must_match_regex(cls, v):
        # regular expression for validating a date
        regex = '%Y-%m-%d'
        if not bool(datetime.strptime(v, regex)):
            raise ValidationError("{}'s is not a valid date.".format(v))
