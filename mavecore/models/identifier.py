from pydantic import BaseModel, ValidationError, validator, HttpUrl
from typing import Optional
import idutils


class Identifier(BaseModel):
    identifier: str
    id: Optional[int]
    url: Optional[HttpUrl]


class DoiIdentifier(Identifier):
    pass


class PubmedIdentifier(Identifier):
    referenceHtml: Optional[str]
