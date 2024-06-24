from limelight.extensions.base import BaseExtension


def test_extension_detection():

    class Animal(BaseExtension):
        __keywords__ = ["dog", "cat", "bird"]

    assert Animal("Brown fox jumps over the lazy dog").enabled is True
    assert Animal("Brown fox is sleeping").enabled is False
