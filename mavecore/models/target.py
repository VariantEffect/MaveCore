from pydantic import BaseModel, ValidationError, validator
from typing import List

from .map import ReferenceMap
from .sequence import WildType


class TargetGene(BaseModel):
    name: str
    category: str
    referenceMaps: List[ReferenceMap]
    wtSequence: WildType
