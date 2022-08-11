from pydantic import BaseModel


class WildType(BaseModel):
    sequenceType: str
    sequence: str
