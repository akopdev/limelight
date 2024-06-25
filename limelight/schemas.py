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


class SearchResults(BaseModel):
    id: str
    query: str
    documents: Optional[List[SearchResultDocument]] = []
    extensions: Optional[List[SearchResultExtension]] = []
