from abc import ABC
from typing import List, Optional

from limelight.models import Document


class BaseExtension(ABC):
    """Base class for all extensions."""

    def __init__(self, query: str):
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

        query = "".join(e for e in self.query if e.isalnum() or e.isspace()).lower()
        keywords = list(set(query.split()))
        return any(keyword in keywords for keyword in self.__keywords__)

    def run(self, documents: Optional[List[Document]] = []):
        raise NotImplementedError
