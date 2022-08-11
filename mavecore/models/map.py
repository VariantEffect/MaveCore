from pydantic import BaseModel
from datetime import datetime

from genome import Genome


class ReferenceMap(BaseModel):
    id: int
    genomeId: int
    targetId: int
    isPrimary: bool
    genome: Genome
    creationDate: datetime
    modificationDate: datetime