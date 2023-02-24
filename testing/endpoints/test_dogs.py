"""
Testing module for Dogs.
"""
from uuid import uuid1

import pytest
from fastapi.testclient import TestClient

from src.models.schemas import Count
from testing.schemas import Animal

BASE_ENDPOINT = "/dogs"


def test_dogs_all(client: TestClient):
    """
    Tests that dogs can be parsed thru the Animal scheme
    """
    # GET /dogs/
    all_dogs, response = Animal.get_all(client=client, endpoint=BASE_ENDPOINT)
    assert response.status_code == 200
    assert all_dogs, "No dogs avalible!"


def test_dogs_count(client: TestClient):
    """
    Tests the amount of dogs compared to the count in a HEAD request.
    """
    all_dogs, response = Animal.get_all(client=client, endpoint=BASE_ENDPOINT)
    assert response.status_code == 200
    dogs_count = Count(**client.get(url="/dogs/count").json())

    assert len(all_dogs) == dogs_count.count


def test_dogs_crud(client: TestClient):
    """
    Tests
    Creating a new dog
    Checking that it is avalible
    Updating the dog fact
    Deleting the dog fact
    """
    test_fact = f"TEST-{uuid1()}"
    updated_test_fact = f"Updated-{test_fact}"

    # GET /dogs/count
    current_amount_of_dogs = Count(**client.get(url="/dogs/count").json()).count

    # POST /dogs/
    created_dog, response = Animal.create(
        client=client,
        endpoint=BASE_ENDPOINT,
        payload={"fact": test_fact},
    )

    assert response.is_success
    assert response.reason_phrase == "OK"
    assert response.status_code == 200

    assert created_dog.fact == test_fact

    # Increased the dog amount by 1!
    assert (
        current_amount_of_dogs + 1
        == Count(**client.get(url="/dogs/count").json()).count
    )

    # GET dogs/{id}
    the_dog, response = Animal.get_one(
        client=client, endpoint=BASE_ENDPOINT, animal_id=created_dog.id
    )
    assert response.status_code == 200
    assert the_dog == created_dog

    # PATCH /dogs/{id}
    updated_dog, response = Animal.update(
        client=client,
        endpoint=BASE_ENDPOINT,
        animal_id=the_dog.id,
        payload={"fact": updated_test_fact},
    )

    assert response.status_code == 200
    assert updated_dog.id == the_dog.id
    assert updated_dog.fact == updated_test_fact
    assert (
        updated_dog.fact
        == Animal.get_one(
            client=client, endpoint=BASE_ENDPOINT, animal_id=updated_dog.id
        )[0].fact
    )

    # DELETE /Dogs/{id}
    response = Animal.delete(
        client=client, endpoint=BASE_ENDPOINT, animal_id=updated_dog.id
    )
    assert response.status_code == 204
    assert response.reason_phrase == "No Content"
    assert response.text == "Fact deleted"

    # Check again if it is really deleted..
    response = Animal.get_one(
        client=client, endpoint=BASE_ENDPOINT, animal_id=updated_dog.id
    )

    assert response.status_code == 404
    assert response.reason_phrase == "Not Found"
    assert response.json() == {"detail": "Fact not found!"}


def test_dogs_fact(client: TestClient):
    """
    Tests a random fact
    """
    random_fact, response = Animal.get_random(client=client, endpoint=BASE_ENDPOINT)
    assert response.status_code == 200

    all_facts, response = Animal.get_all(client=client, endpoint=BASE_ENDPOINT)
    assert random_fact in all_facts
