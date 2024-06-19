from typing import List

import ollama

from .logger import log
from .schemas import QueryMetadata
from .settings import settings
from .storage import Collection


class Query(Collection):
    """
    Query model to store user queries.

    Attributes:
    ----------
        keywords (List[str]): Keywords extracted from the query.
        input (str): Original query text.
        text (str): Corrected query text.
    """

    __collection_name__ = "queries"

    keywords: List[str] = []
    input: str = ""
    summary: str = ""

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
        prompt = (
            "You are an assistant that only speaks JSON.\n"
            "Don't write extra information, don't add Output,\n"
            "don't wrap into markdown code block and don't add additional description.\n"
            "1. Check text grammar and correct it if needed.\n"
            "2. Extract keywords from the query.\n"
            "3. Create a JSON object that includes query and keywords.\n"
            f"Query: '{text}'\n"
            'Example: \'{"query": "<Query with corrected grammar>","keywords": ["word 1", "word 2"]}\''
        )
        try:
            result = ollama.generate(model=settings.language_model, prompt=prompt, stream=False)
            meta = QueryMetadata.model_validate_json(result.get("response", {}))
        except Exception as e:
            log.error(e)
            return
        return cls(keywords=meta.keywords, text=meta.query, input=text)

    def summarise(self, docs: List["Document"]) -> dict:
        """
        Generate a documents summary based on the user query.

        Parameters:
        ----------
            docs (List[Document]): Retrieved documents.

        Returns:
        -------
            str: Summary of the given documents.
        """
        con = "\n".join([doc.text for doc in docs])
        prompt = f"""
        You are an intelligent search engine. You will be provided with some retrieved context, as well as the users query.
        Your job is to understand the request, and answer based on the retrieved context, without adding any new information.
        Try to be as concise and short as possible.
        Here is the retrieved context:
        {con}

        Here is the users query:
        {self.text}
        """

        try:
            result = ollama.generate(model=settings.language_model, prompt=prompt, stream=False)
            self.summary = result.get("response")
        except Exception as e:
            log.error(e)
            return


class Document(Collection):
    __collection_name__ = "documents"

    title: str = ""
    categories: List[str] = []
    url: str = ""
