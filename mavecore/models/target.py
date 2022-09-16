from pydantic import BaseModel, ValidationError, validator
from typing import List, Optional

from .map import ReferenceMap
from .sequence import WildType

from mavecore.validation import target


class TargetGene(BaseModel):
    name: str
    category: str
    ensembleIdId: Optional[int]
    refseqIdId: Optional[int]
    uniprotIdId: Optional[int]
    referenceMaps: List[ReferenceMap]
    wtSequence: WildType

    @validator('category')
    def validate_category(cls, v):
        valid_categories = ["Protein coding", "Regulatory", "Other noncoding"]
        if v not in valid_categories:
            raise ValidationError("{}'s is not a valid target category. Valid categories are "
                                  "Protein coding, Regulatory, and Other noncoding".format(v))
