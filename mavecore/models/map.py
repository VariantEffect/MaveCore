from pydantic import BaseModel


class ReferenceMap(BaseModel):
    genomeId: int
    targetId: int
