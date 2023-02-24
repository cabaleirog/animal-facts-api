"""
This module is meant to represent the pydantic Dog base model
"""

from src.api.models.animal import Animal


class Dog(Animal):  # pylint:disable=too-few-public-methods
    """
    Pydantic model for Dogs
    """
