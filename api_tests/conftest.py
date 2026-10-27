import os

import pytest
from dotenv import load_dotenv

from api_tests.clients.auth_client import AuthClient
from clients.base_client import BaseClient
from clients.pet_client import PetClient
from clients.cookie_client import CookieClient

load_dotenv()

@pytest.fixture(scope="session")
def api_client():
    # Базовый URL публичного (или своего проекта) API для тестов
    base_url = "https://petstore.swagger.io/v2/" # Или чтение из .env!
    client = BaseClient(base_url=base_url)
    yield client
    client.session.close()


@pytest.fixture(scope="session")
def pet_client():
    client = PetClient(base_url=os.getenv("PET_BASE_URL", "https://petstore.swagger.io/v2/"))
    yield client
    client.session.close()



# Новая сессия для каждого теста, Куки не должны ходить между тестами
@pytest.fixture(scope="function")
def echo_client():
    client = CookieClient(base_url=os.getenv("ECHO_URL", "https://postman-echo.com"))
    yield client
    client.session.close()


# Данная фикстура нужна для проверки изоляции (используется после теста с фикстурой echo_client)
@pytest.fixture(scope="function")
def isolated_echo_client():
    client = CookieClient(base_url=os.getenv("ECHO_URL", "https://postman-echo.com"))
    yield client
    client.session.close()

@pytest.fixture(scope="function")
def auth_client():
    client = AuthClient(base_url=os.getenv("REQRES_URL", "https://reqres.in"))
    yield client
    client.session.close()


