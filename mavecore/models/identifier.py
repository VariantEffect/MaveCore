from pydantic import BaseModel, ValidationError, validator, HttpUrl
from typing import Optional
import idutils


class Identifier(BaseModel):
    identifier: str
    id: Optional[int]
    url: Optional[HttpUrl]


class DoiIdentifier(Identifier):

    @validator('identifier')
    def must_match_regular_expression(cls, v):
        if not idutils.is_doi(v):
            raise ValidationError("{} is not a valid DOI identifier.".format(v))


class PubmedIdentifier(Identifier):
    referenceHtml: Optional[str]
