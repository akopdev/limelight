from typing import Optional

from ollama import AsyncClient
from pydantic import BaseModel

from ..logger import log
from ..settings import settings
from .base import BaseExtension


class DocumentSummary(BaseModel):
    """Document summary data."""

    text: Optional[str] = None


class Summary(BaseExtension):
    """
    Extension to generate a summary of the retrieved documents.
    """

    k_top = 3

    @property
    def enabled(self) -> bool:
        # TODO: for now keep summary enabled for all queries
        #       but later we can add some logic to enable it
        #       only for specific queries
        return True

    async def run(self, documents):
        con = "\n".join([doc.text for doc in documents[:self.k_top]])
        prompt = f"""
        You are an intelligent search engine. You will be provided with some retrieved context, as well as the users query.
        Your job is to understand the request, and answer based on the retrieved context, without adding any new information.
        Try to be as concise and short as possible.
        Here is the retrieved context:
        {con}

        Here is the users query:
        {self.query}
        """

        try:
            result = await AsyncClient().generate(
                model=settings.language_model, prompt=prompt, stream=False
            )
            return DocumentSummary(text=result.get("response"))
        except Exception as e:
            log.error(e)
            return
