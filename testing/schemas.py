"""
Schemas
"""
from typing import Any

import httpx
from fastapi.testclient import TestClient
from pydantic import BaseModel  # pylint:disable=no-name-in-module


class Animal(BaseModel):
    """
    Animal model for testing
    """

    id: int
    fact: str

    @classmethod
    def get_all(
        cls,
        client: TestClient,
        endpoint: str,
    ) -> tuple[list["Animal"], httpx.Response]:
        """
        Get all Animal
        """
        response = client.get(url=f"{endpoint}/")
        all_animals = [cls(**animal) for animal in response.json()]
        return all_animals, response

    @classmethod
    def create(
        cls,
        client: TestClient,
        endpoint: str,
        payload: dict[str, Any],
    ) -> tuple["Animal", httpx.Response]:
        """
        Creates an animal.
        """
        response = client.post(
            url=f"{endpoint}/",
            json=payload,
        )
        the_animal = cls(**response.json())
        return the_animal, response

    @classmethod
    def get_one(
        cls,
        client: TestClient,
        endpoint: str,
        animal_id: int,
    ) -> tuple["Animal", httpx.Response] | httpx.Response:
        """
        Get one animal, given a specific id
        """
        response = client.get(url=f"{endpoint}/{animal_id}")
        if response.status_code != 200:
            return response

        the_animal = cls(**response.json())
        return the_animal, response

    @classmethod
    def get_random(
        cls,
        client: TestClient,
        endpoint: str,
    ) -> tuple["Animal", httpx.Response]:
        """
        Get random fact.
        """
        response = client.get(url=f"{endpoint}/fact")
        the_animal = cls(**response.json())
        return the_animal, response

    @classmethod
    def update(
        cls,
        client: TestClient,
        endpoint: str,
        animal_id: int,
        payload: dict[str, Any],
    ) -> tuple["Animal", httpx.Response]:
        """
        Update a Animal fact
        """
        response = client.patch(url=f"{endpoint}/{animal_id}", json=payload)
        the_animal = cls(**response.json())
        return the_animal, response

    @staticmethod
    def delete(client: TestClient, endpoint: str, animal_id: int) -> httpx.Response:
        """
        Returns the response of a DELETE method
        """
        response = client.delete(url=f"{endpoint}/{animal_id}")
        return response
