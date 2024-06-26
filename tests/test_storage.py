from typing import Dict, List

import chromadb
import pytest

from limelight.models import Document, Query
from limelight.storage import Collection


@pytest.fixture(autouse=True)
def _setup(mocker):
    client = chromadb.Client(settings=chromadb.Settings(allow_reset=True))
    client.reset()
    collection = client.get_or_create_collection(name="test_collection")
    mocker.patch("limelight.storage.collection.client", return_value=client)
    mocker.patch.object(Collection, "storage", return_value=collection)


class TestCollection(Document):
    __collection_name__ = "test_collection"

    list_attr: List[str] = []
    dict_attr: Dict[str, str] = {}
    custom_attr: str = ""


def test_restore_collection_document():
    collection = TestCollection(
        id="1234567",
        list_attr=["test 1", "test 2"],
        dict_attr={"custom_key": "custom value"},
        text="It's a test query.",
        custom_attr="custom value",
    )

    assert collection.id == "1234567"
    assert collection.list_attr == ["test 1", "test 2"]
    assert collection.dict_attr == {"custom_key": "custom value"}
    assert collection.text == "It's a test query."
    assert collection.custom_attr == "custom value"


def test_collection_save():
    collection = TestCollection(
        id="1234567",
        text="It's a test query.",
    )

    id = collection.save()

    assert id == "1234567"


def test_collection_get():
    id = TestCollection(text="Test query", list_attr=["key 1", "key 2"]).save()
    collection = TestCollection.get(id)

    assert collection.id == id
    assert collection.text == "Test query"
    assert collection.list_attr == ["key 1", "key 2"]


def test_collection_search(mocker):
    TestCollection(text="It's a test query.").save()
    results = TestCollection.search(Query(text="It's a test query."))

    assert len(results) == 1
    assert results[0].text == "It's a test query."
