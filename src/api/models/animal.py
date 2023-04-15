"""
This module is meant to represent the ABC pydantic model for all Animals.
"""


from pydantic import BaseModel  # pylint: disable=no-name-in-module


class FactModel(BaseModel):  # pylint:disable=too-few-public-methods
    """
    Basemodel for Facts.
    """

    id: int
    fact: str
    animal: str
