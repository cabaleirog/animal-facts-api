"""
Holds the BaseModel for the request body
"""

from pydantic import BaseModel  # pylint:disable=no-name-in-module

from src.api.models.animal import AnimalEnum


class AbstractRequestModel(BaseModel):
    """
    Abstract model for only accepting the FACT payload.
    """

    fact: str


class RequestModel(AbstractRequestModel):
    """
    The request model for payloads with the FACT and ANIMAL values.
    """

    animal: AnimalEnum
