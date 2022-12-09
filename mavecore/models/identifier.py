from pydantic import BaseModel, validator, root_validator
from typing import Optional

from mavecore.validation import identifier as id
from mavecore.validation.utilities import to_camel


class Identifier(BaseModel):
    identifier: str

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class DoiIdentifier(Identifier):

    @validator('identifier')
    def must_be_valid_doi(cls, v):
        id.validate_doi_identifier(v)
        return v


class PubmedIdentifier(Identifier):

    @validator('identifier')
    def must_be_valid_pubmed(cls, v):
        id.validate_pubmed_identifier(v)
        return v


'''class ExternalIdentifierId(BaseModel):
    dbname: str
    identifier: str

    @root_validator(pre=True)
    def check_passwords_match(cls, values):
        print(values.get("dbname"))
        # TODO resolve errors when using root_validator
        #TODO confirm what valid dbname(s) are
        #dbname, dbid = values.get('dbname'), values.get('identifier')
        #print(dbname)
        #print(dbid)
        #if dbname == "sra":
        #    identifier.validate_sra_identifier(dbid)
        #elif dbname == "ensembl":
        #    identifier.validate_ensembl_identifier(dbid)
        #elif dbname == "uniprot":
        #    identifier.validate_uniprot_identifier(dbid)
        #elif dbname == "refseq":
        #    identifier.validate_refseq_identifier(dbid)
        #elif dbname == "genome":
        #    identifier.validate_genome_identifier(dbid)
        #else:
        #    raise ValidationError("dbname must be valid dbname from this list: ")'''


class ExternalIdentifier(BaseModel):
    identifier: dict
    offset: Optional[int]

    class Config:
        alias_generator = to_camel

    @validator('identifier')
    def validate_identifier(cls, v):
        id.validate_external_identifier(v)
        return v
