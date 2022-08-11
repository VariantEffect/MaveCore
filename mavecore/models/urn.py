from pydantic import BaseModel, ValidationError, validator

from ..validation_new.constants.urn import *


class Urn(BaseModel):