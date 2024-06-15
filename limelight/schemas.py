# Description: Schemas for data validation
from typing import List

from pydantic import BaseModel


class QueryMetadata(BaseModel):
    query: str
    keywords: List[str]
