from limelight.skills.base import BaseSkill


def test_skill_detection():

    class Animal(BaseSkill):
        __name__ = "animal"
        __keywords__ = ["dog", "cat", "bird"]

    assert Animal("Brown fox jumps over the lazy dog").enabled is True
    assert Animal("Brown fox is sleeping").enabled is False
