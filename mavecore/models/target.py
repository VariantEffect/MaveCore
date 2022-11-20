from pydantic import BaseModel, validator
from typing import List, Optional

from .map import ReferenceMap
from .sequence import WildType

from mavecore.validation import target
from mavecore.models.identifier import ExternalIdentifier


class TargetGene(BaseModel):
    name: str
    category: str
    externalIdentifiers: List[ExternalIdentifier]
    referenceMaps: List[ReferenceMap]
    wtSequence: WildType

    @validator('category')
    def validate_category(cls, v):
        target.validate_target_category(v)
