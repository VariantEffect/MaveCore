from pydantic import BaseModel

class Identifier(BaseModel):

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