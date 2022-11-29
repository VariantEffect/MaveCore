from pydantic import BaseModel, validator
from typing import List, Optional

from .map import ReferenceMap
from .sequence import WildType

from mavecore.validation import target
from mavecore.models.identifier import ExternalIdentifier
from mavecore.validation.utilities import to_camel


class TargetGene(BaseModel):
    name: str
    category: str
    external_identifiers: List[ExternalIdentifier]
    reference_maps: List[ReferenceMap]
    wt_sequence: WildType

    class Config:
        alias_generator = to_camel

    @validator('category')
    def validate_category(cls, v):
        target.validate_target_category(v)
