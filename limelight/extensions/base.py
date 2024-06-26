from abc import ABC
from typing import List, Optional

from ..models import Document, Query


class BaseExtension(ABC):
    """Base class for all extensions."""

    def __init__(self, query: Query):
        self.query = query

    @property
    def name(self) -> str:
        """
        Get the name of the extension.

        Returns:
        -------
            str: Name of the extension.
        """

        return self.__class__.__name__.lower()

    @property
    def enabled(self) -> bool:
        """
        Check if the extension is applicable for the given query.

        Returns:
        -------
            bool: True if the extension is applicable.
        """
        return any(keyword in self.query.keywords for keyword in self.__keywords__)

    def run(self, documents: Optional[List[Document]] = []):
        raise NotImplementedError
