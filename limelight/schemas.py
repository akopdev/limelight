# Description: Schemas for data validation
from typing import Any, List, Optional

from pydantic import BaseModel


class SearchResultDocument(BaseModel):
    url: str
    title: str
    description: str


class SearchResultExtension(BaseModel):
    name: str
    results: Optional[Any]


class SearchSummary(BaseModel):
    id: str
    text: Optional[str] = ""
    documents: List[SearchResultDocument]


class SearchResults(BaseModel):
    id: str
    query: str
    documents: Optional[List[SearchResultDocument]] = []
    summary: Optional[SearchSummary] = None
    extensions: Optional[List[SearchResultExtension]] = []
