from pydantic import BaseModel, ValidationError, validator
import re


class User(BaseModel):
    orcid_id: str
    firstName: str
    lastName: str
    email: str

    @validator('email')
    def check_email_has_valid_structure(cls, v):
        # regular expression for validating an Email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not (re.fullmatch(regex, v)):
            raise ValueError("{}'s is not a valid email.".format(v))
