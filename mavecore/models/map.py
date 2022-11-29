from pydantic import BaseModel

from mavecore.validation.utilities import to_camel


class ReferenceMap(BaseModel):
    genomeId: int
    targetId: int
