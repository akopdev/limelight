from abc import ABC

from ..models import Query


class BaseExtension(ABC):
    """Base class for all extensions."""

    def __init__(self, query: Query):
        self.query = query

    @property
    def name(self) -> str:
        """
        Get the name of the extension.

        Returns
        -------
            str: Name of the extension.
        """
        return self.__class__.__name__.lower()

    @property
    def enabled(self) -> bool:
        """
        Check if the extension is applicable for the given query.

        Returns
        -------
            bool: True if the extension is applicable. Default is True.
        """
        if getattr(self, "__keywords__", None):
            return any(keyword in self.query.keywords for keyword in self.__keywords__)
        return True
