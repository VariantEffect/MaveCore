from pydantic import BaseModel, ValidationError, validator, HttpUrl
from typing import Optional
import idutils


class Identifier(BaseModel):
    identifier: str
    id: Optional[int]
    url: Optional[HttpUrl]


class DoiIdentifier(Identifier):

    @validator('identifier')
    def must_be_valid_doi(cls, v):
        if not idutils.is_doi(v):
            raise ValidationError("{} is not a valid DOI identifier.".format(v))


class PubmedIdentifier(Identifier):
    referenceHtml: Optional[str]

    @validator('identifier')
    def must_be_valid_pubmed(cls, v):
        if not idutils.is_pmid(v):
            raise ValidationError("{} is not a valid PubMed identifier.".format(v))
