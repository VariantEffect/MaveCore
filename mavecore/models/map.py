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
    creationDate: datetime
    modificationDate: Optional[datetime]