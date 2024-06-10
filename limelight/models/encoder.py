import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer


class Encoder:
    def __init__(self, name: str = "BAAI/bge-small-en-v1.5"):
        self.tokenizer = AutoTokenizer.from_pretrained(name)
        self.model = AutoModel.from_pretrained(name)

        self.tokenizer.save_pretrained("var/model/tokenizer")
        self.model.save_pretrained("var/model/embedding")

    def embedding(self, text: str) -> np.ndarray:
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            vectors = self.model(**inputs).last_hidden_state.mean(dim=1).squeeze()
            return np.array(vectors.tolist())
