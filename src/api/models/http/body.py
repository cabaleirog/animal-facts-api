"""
Holds the BaseModel for the request body
"""

from pydantic import BaseModel  # pylint:disable=no-name-in-module


class RequestBody(BaseModel):  # pylint:disable=too-few-public-methods
    """
    Pydantic model for adding facts
    """

    fact: str
    animal: str
