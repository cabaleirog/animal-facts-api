"""
This module is meant to represent the pydantic Cat base model
"""

from src.api.models.animal import Animal


class Cat(Animal):  # pylint:disable=too-few-public-methods
    """
    Pydantic model for Cats
    """
