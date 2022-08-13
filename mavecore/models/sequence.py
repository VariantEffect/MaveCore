from pydantic import BaseModel, ValidationError, validator


class WildType(BaseModel):
    sequenceType: str
    sequence: str
