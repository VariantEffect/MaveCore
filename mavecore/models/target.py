from pydantic import BaseModel
from typing import List

from map import ReferenceMap
from sequence import WildType


class TargetGene(BaseModel):
    name: str
    category: str
    referenceMaps: list[ReferenceMap]
    wtSequence: WildType
