"""
Testing module for Kangaroos.
"""
from uuid import uuid1

from fastapi.testclient import TestClient

from src.models.schemas import Count
from testing.schemas import Animal

BASE_ENDPOINT = "/kangaroos"


def test_kangaroos_all(client: TestClient):
    """
    Tests that kangaroos can be parsed thru the Animal scheme
    """
    # GET /kangaroos/
    all_kangaroos, response = Animal.get_all(client=client, endpoint=BASE_ENDPOINT)
    assert response.status_code == 200
    assert all_kangaroos, "No kangaroos avalible!"


def test_kangaroos_count(client: TestClient):
    """
    Tests the amount of kangaroos compared to the count in a HEAD request.
    """
    all_kangaroos, response = Animal.get_all(client=client, endpoint=BASE_ENDPOINT)
    assert response.status_code == 200
    kangaroos_count = Count(**client.get(url="/kangaroos/count").json())

    assert len(all_kangaroos) == kangaroos_count.count


def test_kangaroos_crud(client: TestClient):
    """
    Tests
    Creating a new kangaroo
    Checking that it is avalible
    Updating the kangaroo fact
    Deleting the kangaroo fact
    """
    test_fact = f"TEST-{uuid1()}"
    updated_test_fact = f"Updated-{test_fact}"

    # GET /kangaroos/count
    current_amount_of_kangaroos = Count(
        **client.get(url="/kangaroos/count").json()
    ).count

    # POST /kangaroos/
    created_kangaroo, response = Animal.create(
        client=client,
        endpoint=BASE_ENDPOINT,
        payload={"fact": test_fact},
    )

    assert response.is_success
    assert response.reason_phrase == "OK"
    assert response.status_code == 200

    assert created_kangaroo.fact == test_fact

    # Increased the kangaroo amount by 1!
    assert (
        current_amount_of_kangaroos + 1
        == Count(**client.get(url="/kangaroos/count").json()).count
    )

    # GET kangaroos/{id}
    the_kangaroo, response = Animal.get_one(
        client=client, endpoint=BASE_ENDPOINT, animal_id=created_kangaroo.id
    )
    assert response.status_code == 200
    assert the_kangaroo == created_kangaroo

    # PATCH /kangaroos/{id}
    updated_kangaroo, response = Animal.update(
        client=client,
        endpoint=BASE_ENDPOINT,
        animal_id=the_kangaroo.id,
        payload={"fact": updated_test_fact},
    )

    assert response.status_code == 200
    assert updated_kangaroo.id == the_kangaroo.id
    assert updated_kangaroo.fact == updated_test_fact
    assert (
        updated_kangaroo.fact
        == Animal.get_one(
            client=client, endpoint=BASE_ENDPOINT, animal_id=updated_kangaroo.id
        )[0].fact
    )

    # DELETE /Kangaroos/{id}
    response = Animal.delete(
        client=client, endpoint=BASE_ENDPOINT, animal_id=updated_kangaroo.id
    )
    assert response.status_code == 204
    assert response.reason_phrase == "No Content"
    assert response.text == "Fact deleted"

    # Check again if it is really deleted..
    response = Animal.get_one(
        client=client, endpoint=BASE_ENDPOINT, animal_id=updated_kangaroo.id
    )

    assert response.status_code == 404
    assert response.reason_phrase == "Not Found"
    assert response.json() == {"detail": "Fact not found!"}


def test_kangaroos_fact(client: TestClient):
    """
    Tests a random fact
    """
    random_fact, response = Animal.get_random(client=client, endpoint=BASE_ENDPOINT)
    assert response.status_code == 200

    all_facts, response = Animal.get_all(client=client, endpoint=BASE_ENDPOINT)
    assert random_fact in all_facts
