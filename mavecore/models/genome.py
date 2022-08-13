from pydantic import BaseModel, ValidationError, validator
from datetime import datetime
from typing import Optional


class Genome(BaseModel):
    shortName: str
    organismName: str
    genomeId: int
    creationDate: Optional[datetime]
    modificationDate: Optional[datetime]
    id: int

    @validator('creationDate', 'modificationDate')
    def date_must_match_regex(cls, v):
        # regular expression for validating a date
        regex = '%Y-%m-%d'
        if not bool(datetime.strptime(v, regex)):
            raise ValidationError("{}'s is not a valid date.".format(v))
