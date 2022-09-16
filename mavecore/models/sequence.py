from pydantic import BaseModel, ValidationError, validator

from mavecore.validation import target


class WildType(BaseModel):
    sequenceType: str
    sequence: str

    @validator('sequenceType')
    def validate_category(cls, v):
        valid_sequence_types = ["Infer", "DNA", "Protein"]
        if v not in valid_sequence_types:
            raise ValidationError("{}'s is not a valid sequence type. Valid sequence types are "
                                  "Infer, DNA, and Protein".format(v))
