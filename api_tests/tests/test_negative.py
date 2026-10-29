


import pytest

from api_tests.clients import pet_client


class TestBadRequest:
    """Тесты на 400 Bad Request - невалидные данные"""

    def test_create_pet_with_invalid_status(self, pet_client):
        """Создание питомца с невалидным статусов - должен вернцуть 400"""
        invalid_data = {
            "id": 123456,
            "name": "InvalidDog",
            "status": "invalid_status_xyz"
        }

        response = pet_client.create_pet(invalid_data)

        assert response.status_code in [400, 500]

    def test_get_pet_by_invalid_status(self, pet_client):
        """Запрос питомца с невалидным ID"""

        response = pet_client.get_pet_by_id("1234")
        assert response.status_code in [400, 404, 405]

    def test_get_pet_invalid_status(self, pet_client):
        """Поиск питомцев с невалидным статусом"""
        response = pet_client.get_pet_by_status("nonexistent_status")
        assert response.status_code == 400



class TestNotFound:
    """Тесты на отсутствие ресурса - 404"""

    def test_get_pet_by_nonexistent_id(self, pet_client):
        """Запрос питомца с несуществующим ID"""
        response = pet_client.get_pet_by_id(0000000)
        assert response.status_code == 404


    def test_delete_nonexistent_pet(self, pet_client):
        """Удаление несуществующего питомца"""
        response = pet_client.delete_pet(0000000)
        assert response.status_code in [404, 200]

    def test_update_nonexistent_pet(self, pet_client):
        """Обновление несужествующего питомца"""

        update_data = {
            "id": 999999999,
            "name": "Ghost",
            "status": "available"
        }

        response = pet_client.update_pet_full(update_data)
        assert response.status_code in [404, 200]


class TestUnauthorized:
    """Тесты на проблемы авторизации 401 / 403"""

    def test_request_invalid_bearer_token(self, auth_client):
        """Запрос с невалидным Bearer Token"""
        auth_client.set_bearer_token("Invalid_bearer_token")

        response = auth_client.get_users()
        assert response.status_code == 401


    def test_request_with_invalid_api_key(self, pet_client):
        """Запрос с невалидным API Key"""
        pet_client.set_api_key("Invalid_api_key")
        response = pet_client.get_pet_by_status("available")
        assert response.status_code == 401

        pet_client.clear_api_key()