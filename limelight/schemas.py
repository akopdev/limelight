# Description: Schemas for data validation
from typing import List, Optional

from pydantic import BaseModel


class QueryMetadata(BaseModel):
    query: str
    keywords: List[str]


class SearchResultItem(BaseModel):
    url: str
    title: str
    description: str


class SearchResults(BaseModel):
    id: str
    query: str
    results: Optional[List[SearchResultItem]]
