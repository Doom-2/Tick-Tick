import pytest
from rest_framework.test import APIClient
from core.models import User


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture()
def auth_client(client: APIClient, user: User) -> APIClient:
    client.force_login(user)
    return client
