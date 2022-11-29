from pydantic import BaseModel, validator
from typing import List, Dict, Optional

from .identifier import DoiIdentifier, PubmedIdentifier
from .target import TargetGene

from mavecore.validation import keywords, urn
from mavecore.validation.utilities import to_camel


class DataSet(BaseModel):
    title: str
    short_description: str
    abstract_text: str
    method_text: str
    extra_metadata: Optional[Dict]
    keywords: Optional[List[str]]

    class Config:
        alias_generator = to_camel

    @validator('keywords')
    def validate_keywords(cls, v):
        keywords.validate_keywords(v)


class Experiment(DataSet):
    doi_identifiers: Optional[List[DoiIdentifier]]
    pubmed_identifiers: Optional[List[PubmedIdentifier]]


class ScoreSet(DataSet):
    data_usage_policy: str
    licence_id: int
    experiment_urn: str
    superseded_scoreset_urn: Optional[str]
    meta_analysis_source_scoreset_urns: Optional[List[str]]
    doi_identifiers: Optional[List[DoiIdentifier]]
    pubmed_identifiers: Optional[List[PubmedIdentifier]]
    target_gene: TargetGene

    @validator('superseded_scoresetUrn', 'meta_analysis_source_scoreset_urns')
    def validate_scoreset_urn(cls, v):
        if type(v) == str:
            urn.validate_mavedb_urn_scoreset(v)
        else:
            [urn.validate_mavedb_urn_scoreset(s) for s in v]

    @validator('experiment_urn')
    def validate_experiment_urn(cls, v):
        urn.validate_mavedb_urn_experiment(v)
