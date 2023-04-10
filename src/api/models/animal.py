"""
This module is meant to represent the ABC pydantic model for all Animals.
"""


from pydantic import BaseModel  # pylint: disable=no-name-in-module


class Animal(BaseModel):  # pylint:disable=too-few-public-methods
    """
    Basemodel for Animals.
    This is where all other animal types will derive from.
    """

    id: int
    fact: str
