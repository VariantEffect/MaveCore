from pydantic import BaseModel, ValidationError, validator, HttpUrl
from typing import Optional

from mavecore.validation import identifier


class Identifier(BaseModel):
    identifier: str
    id: Optional[int]
    url: Optional[HttpUrl]


class DoiIdentifier(Identifier):

    @validator('identifier')
    def must_be_valid_doi(cls, v):
        identifier.validate_doi_identifier(v)


class PubmedIdentifier(Identifier):
    referenceHtml: Optional[str]

    @validator('identifier')
    def must_be_valid_pubmed(cls, v):
        identifier.validate_pubmed_identifier(v)
