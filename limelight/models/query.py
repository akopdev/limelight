import time
from typing import List

import torch
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer

from limelight.logger import log

model_name = "microsoft/Phi-3-mini-4k-instruct"


device = torch.device("cpu")
model = AutoModelForCausalLM.from_pretrained(model_name, local_files_only=True).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name)


class QueryProcess(BaseModel):
    query: str
    keywords: List[str]


class Query:

    text: str

    def __init__(self, q: str):
        self.text = q.strip()

    def process(self) -> str:
        prompt = (
            """
You are an assistant that only speaks JSON.
Don't write extra information, don't add Output: or anything else.
1. Check text grammar and correct it if needed.
2. Extract keywords from the query.
3. Create a JSON object that includes query and keywords.
Query: '"""
            + self.text
            + """'
Example: '
    {"query": "<Query with corrected grammar>","keywords": ["keyword 1", "keyword 2"]}'
        """
        )
        generation_args = {
            "max_new_tokens": 500,
            "do_sample": True,
        }

        inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=True).to(device)
        start = time.time()
        print("start")

        outputs = model.generate(inputs.input_ids, **generation_args)
        text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        end = time.time() - start

        print("Generating took: " + str(end))

        result = text[len(prompt) :]
        log.error(result)

        try:
            return QueryProcess.model_validate_json(result)
        except Exception as e:
            log.error(e)
