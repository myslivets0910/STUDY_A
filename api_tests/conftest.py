import pytest
from clients.base_client import BaseClient
from clients.pet_client import PetClient

@pytest.fixture(scope="session")
def api_client():
    # Базовый URL публичного (или своего проекта) API для тестов
    base_url = "https://petstore.swagger.io/v2/"
    client = BaseClient(base_url=base_url)
    yield client
    client.session.close()


@pytest.fixture(scope="session")
def pet_client():
    base_url = "https://petstore.swagger.io/v2/"
    client = PetClient(base_url = base_url)
    yield client
    client.session.close()

