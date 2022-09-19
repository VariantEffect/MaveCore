from pydantic import BaseModel, ValidationError, validator, HttpUrl
from typing import Optional

from mavecore.validation import identifier


class Identifier(BaseModel):
    identifier: str


class DoiIdentifier(Identifier):

    @validator('identifier')
    def must_be_valid_doi(cls, v):
        identifier.validate_doi_identifier(v)


class PubmedIdentifier(Identifier):

    @validator('identifier')
    def must_be_valid_pubmed(cls, v):
        identifier.validate_pubmed_identifier(v)


class ExternalIdentifierId(BaseModel):
    dbname: str
    identifier: str


class ExternalIdentifier(BaseModel):
    identifier: ExternalIdentifierId
    offset: int
