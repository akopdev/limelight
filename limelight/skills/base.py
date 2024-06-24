from abc import ABC


class BaseSkill(ABC):
    """Base class for all skills."""

    def __init__(self, query: str):
        self.query = query

    @property
    def name(self) -> str:
        """
        Get the name of the skill.

        Returns:
        -------
            str: Name of the skill.
        """

        return self.__name__ or "unknown"

    @property
    def enabled(self) -> bool:
        """
        Check if the skill is applicable for the given query.

        Returns:
        -------
            bool: True if the skill is applicable.
        """

        query = "".join(e for e in self.query if e.isalnum() or e.isspace()).lower()
        keywords = list(set(query.split()))
        return any(keyword in keywords for keyword in self.__keywords__)

    def run(self):
        raise NotImplementedError
