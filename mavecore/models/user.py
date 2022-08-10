from pydantic import BaseModel

class User(BaseModel):
    {
        "orcid_id": "string",
        "firstName": "string",
        "lastName": "string",
        "email": "string"
    },