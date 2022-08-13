from pydantic import BaseModel, ValidationError, validator
from datetime import datetime
from typing import Optional

from .genome import Genome


class ReferenceMap(BaseModel):
    id: int
    genomeId: int
    targetId: int
    isPrimary: bool
    genome: Genome
    creationDate: Optional[str]
    modificationDate: Optional[str]

    @validator('creationDate', 'modificationDate')
    def date_must_match_regex(cls, v):
        # regular expression for validating a date
        regex = '%Y-%m-%d'
        if not bool(datetime.strptime(v, regex)):
            raise ValidationError("{}'s is not a valid date.".format(v))
