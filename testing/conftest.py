"""
Conftest file for fixtures.
"""
import pytest
from fastapi.testclient import TestClient

from src.api.main import app


@pytest.fixture(scope="module")
def client() -> TestClient:
    """
    Return the TestClient
    """

    return TestClient(
        app=app,
        base_url="http://animaltesting",
        raise_server_exceptions=True,
        root_path="",
        backend="asyncio",
        backend_options=None,
    )
