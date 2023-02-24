"""
This module is meant to represent the pydantic Kangaroo base model
"""

from src.api.models.animal import Animal


class Kangaroo(Animal):  # pylint:disable=too-few-public-methods
    """
    Pydantic model for Kangaroos
    """
