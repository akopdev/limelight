from limelight.extensions.base import BaseExtension
from limelight.models import Query


def test_extension_detection():
    class Animal(BaseExtension):
        __keywords__ = ["dog", "cat", "bird"]

    q1 = Query(text="Brown fox jumps over the lazy dog", keywords=["brown", "fox", "lazy", "dog"])
    q2 = Query(text="Brown fox is sleeping", keywords=["brown", "fox", "sleeping"])

    assert Animal(q1).enabled is True
    assert Animal(q2).enabled is False
