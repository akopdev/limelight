from typing import List

import numpy as np
from ollama import AsyncClient
from pydantic import BaseModel

from .logger import log
from .settings import settings


class QueryMetadata(BaseModel):
    query: str
    keywords: List[str]


async def embedding(text: str) -> np.ndarray:
    try:
        response = await AsyncClient().embeddings(
            model=settings.embedding_model,
            prompt=text,
        )
        return np.array(response["embedding"].tolist())
    except Exception as e:
        log.error(e)


async def process_query(text):
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
        result = await AsyncClient().generate(
            model=settings.language_model, prompt=prompt, stream=False
        )
        return QueryMetadata.model_validate_json(result.get("response", {}))
    except Exception as e:
        log.error(e)
        return
