"""
This module is meant to represent the pydantic Fox base model
"""

from src.api.models.animal import Animal


class Fox(Animal):  # pylint:disable=too-few-public-methods
    """
    Pydantic model for Foxes
    """
