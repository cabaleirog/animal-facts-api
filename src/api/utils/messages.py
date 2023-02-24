"""
This module is meant to represent a Message, usually for ERROR handling.
"""

from pydantic import BaseModel  # pylint:disable=no-name-in-module


class Message(BaseModel):
    """Error handling messages."""

    message: str
