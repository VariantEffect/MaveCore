from pydantic import BaseModel, HttpUrl


class Identifier(BaseModel):
    identifier: str
    id: 0
    url: HttpUrl


class DoiIdentifier(Identifier):
    {
        "identifier": "string",
        "id": 0,
        "url": "string"
    }

class PubmedIdentifier(Identifier):
    {
        "identifier": "string",
        "id": 0,
        "url": "string",
        "referenceHtml": "string"
    }