"""
Conftest file for fixtures.
"""
from typing import Iterator

import pytest
from httpx import Client


@pytest.fixture(scope="session")
def client() -> Iterator[Client]:
    """
    Return the TestClient
    """
    with Client(base_url="http://localhost:8080") as _client:
        try:
            yield _client
        finally:
            _client.close()
