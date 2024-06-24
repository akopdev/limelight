import json
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

import chromadb

from limelight.settings import settings

client = chromadb.PersistentClient(path=settings.storage_path)


class Collection:
    id: str
    text: str

    def __init__(self, **kwargs) -> None:
        self.id = str(uuid4())
        self.text = ""

        annotations = list(self.__annotations__.keys()) + ["id", "text"]
        for index, value in kwargs.items():
            if index in annotations:
                setattr(self, index, value)

    def _serialize_metadata(self) -> Dict[str, str]:
        result = {}
        for key, value in self.__annotations__.items():
            if hasattr(value, "__origin__"):
                if value.__origin__ == list:
                    result[key] = ",".join(getattr(self, key))
                elif value.__origin__ == dict:
                    result[key] = json.dumps(getattr(self, key))
                else:
                    result[key] = getattr(self, key)
            else:
                result[key] = getattr(self, key)
        return result

    @classmethod
    def _unserialize_metadata(
        self, metadata: Dict[str, Union[str, int, float]] = {}
    ) -> Dict[str, Any]:
        result = {}
        for key, value in metadata.items():
            if key in self.__annotations__:
                if hasattr(self.__annotations__[key], "__origin__"):
                    if self.__annotations__[key].__origin__ == list:
                        result[key] = value.split(",")
                    elif self.__annotations__[key].__origin__ == dict:
                        result[key] = json.loads(value)
                    else:
                        result[key] = value
                else:
                    result[key] = value
        return result

    def save(self) -> str:
        self.storage().upsert(
            ids=[self.id],
            documents=[self.text],
            metadatas=[self._serialize_metadata()],
        )
        return self.id

    @classmethod
    def storage(cls) -> "Collection":
        return client.get_or_create_collection(name=cls.__collection_name__)

    @classmethod
    def get(cls, id: str) -> "Collection":
        items = cls.storage().get(ids=[id])
        if items["documents"]:
            return cls(
                id=items["ids"][0],
                text=items["documents"][0],
                **cls._unserialize_metadata(items["metadatas"][0])
            )

    @classmethod
    def search(
        cls, text: str, filter: Optional[List[str]] = [], limit: int = 10
    ) -> List["Collection"]:
        extra = {
            "n_results": limit,
        }
        if filter:
            if len(filter) == 1:
                extra["where_document"] = {"$contains": filter[0]}
            else:
                extra["where_document"] = {"$or": [{"$contains": f} for f in filter]}
        items = cls.storage().query(query_texts=[text], **extra)
        return [
            cls(
                id=items["ids"][0][i],
                text=text,
                **cls._unserialize_metadata(items["metadatas"][0][i])
            )
            for i, text in enumerate(items["documents"][0])
        ]

    def __str__(self) -> str:
        return self.text
