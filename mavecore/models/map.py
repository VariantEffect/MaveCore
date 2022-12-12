from pydantic import BaseModel

from mavecore.validation.utilities import to_camel


class ReferenceMap(BaseModel):
    genome_id: int
    target_id: int

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
