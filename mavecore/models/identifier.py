from pydantic import BaseModel, HttpUrl


class Identifier(BaseModel):
    identifier: str
    id: 0
    url: HttpUrl


class DoiIdentifier(Identifier):
    pass


class PubmedIdentifier(Identifier):
    {
        "identifier": "string",
        "id": 0,
        "url": "string",
        "referenceHtml": "string"
    }