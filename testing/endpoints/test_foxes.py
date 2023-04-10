"""
Testing module for Cats.
"""
from uuid import uuid1

import pytest
from fastapi.testclient import TestClient

from src.models.schemas import Count
from testing.schemas import Animal

BASE_ENDPOINT = "/fox"


def test_fox_all(client: TestClient):
    """
    Tests that fox can be parsed thru the Animal scheme
    """
    # GET /fox/
    all_foxes, response = Animal.get_all(client=client, endpoint=BASE_ENDPOINT)
    assert response.status_code == 200
    assert all_foxes, "No fox avalible!"


def test_fox_count(client: TestClient):
    """
    Tests the amount of fox compared to the count in a HEAD request.
    """
    all_foxes, response = Animal.get_all(client=client, endpoint=BASE_ENDPOINT)
    assert response.status_code == 200
    fox_count = Count(**client.get(url="/fox/count").json())

    assert len(all_foxes) == fox_count.count


def test_fox_crud(client: TestClient):
    """
    Tests
    Creating a new fox
    Checking that it is avalible
    Updating the fox fact
    Deleting the fox fact
    """
    test_fact = f"TEST-{uuid1()}"
    updated_test_fact = f"Updated-{test_fact}"

    # GET /fox/count
    current_amount_of_fox = Count(**client.get(url="/fox/count").json()).count

    # POST /fox/
    created_fox, response = Animal.create(
        client=client,
        endpoint=BASE_ENDPOINT,
        payload={"fact": test_fact},
    )

    assert response.is_success
    assert response.reason_phrase == "OK"
    assert response.status_code == 200

    assert created_fox.fact == test_fact

    # Increased the fox amount by 1!
    assert (
        current_amount_of_fox + 1 == Count(**client.get(url="/fox/count").json()).count
    )

    # GET fox/{id}
    the_fox, response = Animal.get_one(
        client=client, endpoint=BASE_ENDPOINT, animal_id=created_fox.id
    )
    assert response.status_code == 200
    assert the_fox == created_fox

    # PATCH /fox/{id}
    updated_fox, response = Animal.update(
        client=client,
        endpoint=BASE_ENDPOINT,
        animal_id=the_fox.id,
        payload={"fact": updated_test_fact},
    )

    assert response.status_code == 200
    assert updated_fox.id == the_fox.id
    assert updated_fox.fact == updated_test_fact
    assert (
        updated_fox.fact
        == Animal.get_one(
            client=client, endpoint=BASE_ENDPOINT, animal_id=updated_fox.id
        )[0].fact
    )

    # DELETE /Cats/{id}
    response = Animal.delete(
        client=client, endpoint=BASE_ENDPOINT, animal_id=updated_fox.id
    )
    assert response.status_code == 204
    assert response.reason_phrase == "No Content"
    assert response.text == "Fact deleted"

    # Check again if it is really deleted..
    response = Animal.get_one(
        client=client, endpoint=BASE_ENDPOINT, animal_id=updated_fox.id
    )

    assert response.status_code == 404
    assert response.reason_phrase == "Not Found"
    assert response.json() == {"detail": "Fact not found!"}


def test_fox_fact(client: TestClient):
    """
    Tests a random fact
    """
    random_fact, response = Animal.get_random(client=client, endpoint=BASE_ENDPOINT)
    assert response.status_code == 200

    all_facts, response = Animal.get_all(client=client, endpoint=BASE_ENDPOINT)
    assert random_fact in all_facts
