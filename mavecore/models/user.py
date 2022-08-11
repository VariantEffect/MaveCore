from pydantic import BaseModel


class User(BaseModel):
    orcid_id: str
    firstName: str
    lastName: str
    email: str
