from typing import List

import ollama

from .logger import log
from .settings import settings
from .storage import Collection


class Query(Collection):
    """
    Query model to store user queries.

    Attributes
    ----------
        input (str): Original query text.
        text (str): Corrected query text.
    """

    __collection_name__ = "queries"

    input: str = ""
    keywords: List[str] = []

    @classmethod
    def parse_text(cls, input: str) -> "Query":
        """
        Parse the user query, correct grammar and extract keywords.

        Parameters
        ----------
            input (str): User query text.

        Returns
        -------
            Query: Query object with keywords and corrected text.
        """
        try:
            result = ollama.generate(model=settings.grammar_model, prompt=input, stream=False)
            text = result.get("response", input)
            # TODO: Extract keywords from the text
            keywords = text.split()
            return cls(text=text, input=text, keywords=keywords)
        except Exception as e:
            log.error(e)


class Document(Collection):
    __collection_name__ = "documents"

    title: str = ""
    categories: List[str] = []
    url: str = ""

    @classmethod
    def search(cls, query: Query, limit: int = 10) -> List["Collection"]:
        extra = {
            "n_results": limit,
        }
        if query.keywords:
            if len(query.keywords) == 1:
                extra["where_document"] = {"$contains": query.keywords[0]}
            else:
                extra["where_document"] = {"$or": [{"$contains": f} for f in query.keywords]}
        items = cls.storage().query(query_texts=[query.text], **extra)
        return [
            cls(
                id=items["ids"][0][i],
                text=text,
                **cls._unserialize_metadata(items["metadatas"][0][i]),
            )
            for i, text in enumerate(items["documents"][0])
        ]


class Summary(Collection):
    __collection_name__ = "summaries"

    documents: List[str] = []
    query: str = ""

    def generate(self) -> str:
        con = "\n".join([Document.get(doc).text for doc in self.documents])
        prompt = f"""
        You are an intelligent search engine. You will be provided with some retrieved context,
        as well as the users query. Your job is to understand the request, and answer based on
        the retrieved context, without adding any new information.
        Try to be as concise and short as possible.
        Here is the retrieved context:
        {con}

        Here is the users query:
        {self.query}
        """

        try:
            resp = ollama.generate(model=settings.language_model, prompt=prompt, stream=False)
            self.text = resp.get("response", "")
            self.save()
        except Exception as e:
            log.error(e)
            return
