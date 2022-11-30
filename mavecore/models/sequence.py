from pydantic import BaseModel, validator

from mavecore.validation import target
from mavecore.validation.utilities import to_camel


class WildType(BaseModel):
    sequence_type: str
    sequence: str

    class Config:
        alias_generator = to_camel

    @validator('sequence_type')
    def validate_category(cls, v):
        target.validate_sequence_category(v)

    @validator('sequence')
    def validate_sequence(cls, v):
        target.validate_target_sequence(v)
