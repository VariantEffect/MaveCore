from pydantic import BaseModel, HttpUrl
from typing import Optional


class Identifier(BaseModel):
    identifier: str
    id: Optional[0]
    url: Optional[HttpUrl]


class DoiIdentifier(Identifier):
    pass


class PubmedIdentifier(Identifier):
    referenceHtml: Optional[str]
