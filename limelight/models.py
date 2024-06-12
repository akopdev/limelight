from typing import List
from limelight.storage import Collection


class Query(Collection):
    __collection_name__ = "queries"

    keywords: List[str] = []
