from pydantic import BaseModel, HttpUrl
from typing import Optional


class Identifier(BaseModel):
    identifier: str
    id: 0
    url: HttpUrl


class DoiIdentifier(Identifier):
    pass


class PubmedIdentifier(Identifier):
    referenceHtml: str
