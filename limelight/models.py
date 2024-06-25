from typing import List

import ollama

from .logger import log
from .settings import settings
from .storage import Collection


class Query(Collection):
    """
    Query model to store user queries.

    Attributes:
    ----------
        input (str): Original query text.
        text (str): Corrected query text.
    """

    __collection_name__ = "queries"

    input: str = ""

    @classmethod
    def parse_text(cls, text) -> "Query":
        """
        Parse the user query, correct grammar and extract keywords.

        Parameters:
        ----------
            text (str): User query text.

        Returns:
        -------
            Query: Query object with keywords and corrected text.
        """
        try:
            result = ollama.generate(model=settings.grammar_model, prompt=text, stream=False)
            return cls(text=result.get("response", text), input=text)
        except Exception as e:
            log.error(e)
            return


class Document(Collection):
    __collection_name__ = "documents"

    title: str = ""
    categories: List[str] = []
    url: str = ""
