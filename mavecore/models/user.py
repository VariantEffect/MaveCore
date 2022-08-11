from pydantic import BaseModel, ValidationError, validator
import re

from ..validation_new.exceptions import ValidationError


class User(BaseModel):
    orcid_id: str
    firstName: str
    lastName: str
    email: str
