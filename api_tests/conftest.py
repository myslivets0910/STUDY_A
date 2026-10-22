import pytest
from clients.base_client import BaseClient
from clients.pet_client import PetClient
from clients.cookie_client import CookieClient

@pytest.fixture(scope="session")
def api_client():
    # Базовый URL публичного (или своего проекта) API для тестов
    base_url = "https://petstore.swagger.io/v2/" # Или чтение из .env!
    client = BaseClient(base_url=base_url)
    yield client
    client.session.close()


@pytest.fixture(scope="session")
def pet_client():
    base_url = "https://petstore.swagger.io/v2/" # Или чтение из .env!
    client = PetClient(base_url = base_url)
    yield client
    client.session.close()


# Новая сессия для каждого теста, Куки не должны ходить между тестами
@pytest.fixture(scope="function")
def echo_client():
    base_url = "https://postman-echo.com"
    client = CookieClient(base_url = base_url)
    yield client
    client.session.close()


# Данная фикстура нужна для проверки изоляции (используется после теста с фикстурой echo_client)
@pytest.fixture(scope="function")
def isolated_echo_client():
    base_url = "https://postman-echo.com"
    client = CookieClient(base_url = base_url)
    yield client
    client.session.close()
