from pydantic import BaseModel
from datetime import datetime


class Genome(BaseModel):
    shortName: str
    organismName: str
    genomeId: int
    creationDate: datetime
    modificationDate: datetime
    id: int
