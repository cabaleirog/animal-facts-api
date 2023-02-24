"""
Testing module for Birds.
"""
from uuid import uuid1

import httpx
from fastapi.testclient import TestClient

from src.models.schemas import Count
from testing.schemas import Animal

BASE_ENDPOINT = "/birds"


def test_birds_all(client: TestClient):
    """
    Tests that birds can be parsed thru the Animal scheme
    """
    # GET /birds/
    all_birds, response = Animal.get_all(client=client, endpoint=BASE_ENDPOINT)
    assert response.status_code == 200
    assert all_birds, "No birds avalible!"


def test_birds_count(client: TestClient):
    """
    Tests the amount of birds compared to the count in a HEAD request.
    """
    all_birds, response = Animal.get_all(client=client, endpoint=BASE_ENDPOINT)
    assert response.status_code == 200
    birds_count = Count(**client.get(url="/birds/count").json())

    assert len(all_birds) == birds_count.count


def test_birds_crud(client: TestClient):
    """
    Tests
    Creating a new bird
    Checking that it is avalible
    Updating the bird fact
    Deleting the bird fact
    """
    test_fact = f"TEST-{uuid1()}"
    updated_test_fact = f"Updated-{test_fact}"

    # GET /birds/count
    current_amount_of_birds = Count(**client.get(url="/birds/count").json()).count

    # POST /birds/
    created_bird, response = Animal.create(
        client=client,
        endpoint=BASE_ENDPOINT,
        payload={"fact": test_fact},
    )

    assert response.is_success
    assert response.reason_phrase == "OK"
    assert response.status_code == 200

    assert created_bird.fact == test_fact

    # Increased the bird amount by 1!
    assert (
        current_amount_of_birds + 1
        == Count(**client.get(url="/birds/count").json()).count
    )

    # GET birds/{id}
    the_bird, response = Animal.get_one(
        client=client,
        endpoint=BASE_ENDPOINT,
        animal_id=created_bird.id,
    )
    assert response.status_code == 200
    assert the_bird == created_bird

    # PATCH /birds/{id}
    updated_bird, response = Animal.update(
        client=client,
        endpoint=BASE_ENDPOINT,
        animal_id=the_bird.id,
        payload={"fact": updated_test_fact},
    )

    assert response.status_code == 200
    assert updated_bird.id == the_bird.id
    assert updated_bird.fact == updated_test_fact
    assert (
        updated_bird.fact
        == Animal.get_one(
            client=client,
            endpoint=BASE_ENDPOINT,
            animal_id=updated_bird.id,
        )[0].fact
    )

    # DELETE /Birds/{id}
    response = Animal.delete(
        client=client, endpoint=BASE_ENDPOINT, animal_id=updated_bird.id
    )
    assert response.status_code == 204
    assert response.reason_phrase == "No Content"
    assert response.text == "Fact deleted"

    # Check again if it is really deleted..
    response: httpx.Response = Animal.get_one(
        client=client, endpoint=BASE_ENDPOINT, animal_id=updated_bird.id
    )

    assert response.status_code == 404
    assert response.reason_phrase == "Not Found"
    assert response.json() == {"detail": "Fact not found!"}


def test_birds_fact(client: TestClient):
    """
    Tests a random fact
    """
    random_fact, response = Animal.get_random(client=client, endpoint=BASE_ENDPOINT)
    assert response.status_code == 200

    all_facts, response = Animal.get_all(client=client, endpoint=BASE_ENDPOINT)
    assert random_fact in all_facts
