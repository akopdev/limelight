from typing import List

import ollama

from .logger import log
from .models import Document, Query
from .settings import settings


def combine_response(docs: List[Document], query: Query):
    con = "\n".join([doc.text for doc in docs])
    prompt = f"""
    You are an intelligent search engine. You will be provided with some retrieved context, as well as the users query.
    Your job is to understand the request, and answer based on the retrieved context.
    Here is the retrieved context:
    {con}

    Here is the users query:
    {query}
    """

    try:
        result = ollama.generate(model=settings.language_model, prompt=prompt, stream=False)
        return result.get("response", {})
    except Exception as e:
        log.error(e)
        return
