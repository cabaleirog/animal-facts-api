"""
Testing module for Cats.
"""
from uuid import uuid1

import pytest
from fastapi.testclient import TestClient

from src.models.schemas import Count
from testing.schemas import Animal

BASE_ENDPOINT = "/cats"


def test_cats_all(client: TestClient):
    """
    Tests that cats can be parsed thru the Animal scheme
    """
    # GET /cats/
    all_cats, response = Animal.get_all(client=client, endpoint=BASE_ENDPOINT)
    assert response.status_code == 200
    assert all_cats, "No cats avalible!"


def test_cats_count(client: TestClient):
    """
    Tests the amount of cats compared to the count in a HEAD request.
    """
    all_cats, response = Animal.get_all(client=client, endpoint=BASE_ENDPOINT)
    assert response.status_code == 200
    cats_count = Count(**client.get(url="/cats/count").json())

    assert len(all_cats) == cats_count.count


def test_cats_crud(client: TestClient):
    """
    Tests
    Creating a new cat
    Checking that it is avalible
    Updating the cat fact
    Deleting the cat fact
    """
    test_fact = f"TEST-{uuid1()}"
    updated_test_fact = f"Updated-{test_fact}"

    # GET /cats/count
    current_amount_of_cats = Count(**client.get(url="/cats/count").json()).count

    # POST /cats/
    created_cat, response = Animal.create(
        client=client,
        endpoint=BASE_ENDPOINT,
        payload={"fact": test_fact},
    )

    assert response.is_success
    assert response.reason_phrase == "OK"
    assert response.status_code == 200

    assert created_cat.fact == test_fact

    # Increased the cat amount by 1!
    assert (
        current_amount_of_cats + 1
        == Count(**client.get(url="/cats/count").json()).count
    )

    # GET cats/{id}
    the_cat, response = Animal.get_one(
        client=client, endpoint=BASE_ENDPOINT, animal_id=created_cat.id
    )
    assert response.status_code == 200
    assert the_cat == created_cat

    # PATCH /cats/{id}
    updated_cat, response = Animal.update(
        client=client,
        endpoint=BASE_ENDPOINT,
        animal_id=the_cat.id,
        payload={"fact": updated_test_fact},
    )

    assert response.status_code == 200
    assert updated_cat.id == the_cat.id
    assert updated_cat.fact == updated_test_fact
    assert (
        updated_cat.fact
        == Animal.get_one(
            client=client, endpoint=BASE_ENDPOINT, animal_id=updated_cat.id
        )[0].fact
    )

    # DELETE /Cats/{id}
    response = Animal.delete(
        client=client, endpoint=BASE_ENDPOINT, animal_id=updated_cat.id
    )
    assert response.status_code == 204
    assert response.reason_phrase == "No Content"
    assert response.text == "Fact deleted"

    # Check again if it is really deleted..
    response = Animal.get_one(
        client=client, endpoint=BASE_ENDPOINT, animal_id=updated_cat.id
    )

    assert response.status_code == 404
    assert response.reason_phrase == "Not Found"
    assert response.json() == {"detail": "Fact not found!"}


def test_cats_fact(client: TestClient):
    """
    Tests a random fact
    """
    random_fact, response = Animal.get_random(client=client, endpoint=BASE_ENDPOINT)
    assert response.status_code == 200

    all_facts, response = Animal.get_all(client=client, endpoint=BASE_ENDPOINT)
    assert random_fact in all_facts
