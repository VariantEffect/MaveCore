from pydantic import BaseModel, validator

from mavecore.validation import target


class WildType(BaseModel):
    sequenceType: str
    sequence: str

    @validator('sequenceType')
    def validate_category(cls, v):
        target.validate_sequence_category(v)
