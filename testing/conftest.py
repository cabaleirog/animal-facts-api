"""
Conftest file for fixtures.
"""
import os
from typing import Iterator

import pytest
from httpx import Client

# _ENV = os.getenv("DOCKER_HOST", "http://0.0.0.0:8080")


@pytest.fixture(scope="session")
def client() -> Iterator[Client]:
    """
    Return the TestClient
    """
    with Client(base_url="http://project_appnet:8080") as _client:
        try:
            yield _client
        finally:
            _client.close()
