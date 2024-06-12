from uuid import uuid4

import chromadb

from limelight.settings import settings

client = chromadb.PersistentClient(path=settings.storage_path)


class Collection:

    id: str
    text: str

    def __init__(self, **kwargs) -> None:
        self.__collection = client.get_or_create_collection(name=self.__collection_name__)
        self.id = str(uuid4())
        self.text = ""

        for index, value in kwargs.items():
            if hasattr(self, index):
                setattr(self, index, value)

    def save(self):
        return self.__collection.add(
            ids=[self.id],
            documents=[self.text],
            metadatas=[{key: getattr(self, key) for key in self.__annotations__.keys()}],
        )

    @classmethod
    def search(self, text: str, limit: int = 10):
        collection = client.get_or_create_collection(name=self.__collection_name__)
        items = collection.query(
            query_texts=[text],
            n_results=limit,
        )
        return [
            self(
                id=items["ids"][0][i],
                text=text,
                **items["metadatas"][0][i],
            )
            for i, text in enumerate(items["documents"][0])
        ]
