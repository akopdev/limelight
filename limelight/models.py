from typing import List

from .storage import Collection


class Query(Collection):
    __collection_name__ = "queries"

    keywords: List[str] = []
