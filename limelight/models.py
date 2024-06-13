from typing import List

from .storage import Collection


class Query(Collection):
    __collection_name__ = "queries"

    keywords: List[str] = []


class Document(Collection):
    __collection_name__ = "documents"

    title: str = ""
    categories: List[str] = []
