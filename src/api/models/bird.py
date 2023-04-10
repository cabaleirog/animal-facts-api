"""
This module is meant to represent the pydantic Bird base model
"""


from src.api.models.animal import Animal


class Bird(Animal):  # pylint:disable=too-few-public-methods
    """
    Pydantic model for Birds
    """
