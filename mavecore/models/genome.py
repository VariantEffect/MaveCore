from pydantic import BaseModel, ValidationError, validator
from datetime import datetime
from typing import Optional


class Genome(BaseModel):
    shortName: str
    organismName: str
    genomeId: int
    creationDate: datetime
    modificationDate: Optional[datetime]
    id: int
