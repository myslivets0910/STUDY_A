

import pytest


class TestApiKey:
    """Тесты на API Key авторизацию"""

    def test_set_api_key_in_headers(self, pet_client):
        """Проверям что ключ есть в загаловке"""
        pet_client.set_api_key("special-key")

        assert "api_key" in pet_client.session.headers
        assert pet_client.session.headers["api_key"] == "special-key"

        pet_client.clear_api_key()


    def test_request_with_api_key(self, pet_client):
        """Проверяем отправку запроса в АPI Key"""

        pet_client.set_api_key("special-key")

        response = pet_client.get_pet_by_status("available")
        assert response.status_code == 200

        pet_client.clear_api_key()


    def test_clear_api_key(self, pet_client):

        pet_client.set_api_key("special-key")
        assert "api_key" in pet_client.session.headers

        pet_client.clear_api_key()
        assert "api_key" not in pet_client.session.headers



    def test_multiple_auth_methods_in_session(self, pet_client):
        """ПРоверка на то что в одной сессии может быть несколько типов авторизаций"""
        pet_client.set_api_key("special-key")
        pet_client.session.headers.update({"Authorization": "Bearer fake-token"})

        assert "api_key" in pet_client.session.headers
        assert "Authorization" in pet_client.session.headers


        # Очистка обоих

        pet_client.clear_api_key()
        if "Authorization" in pet_client.session.headers:
            del pet_client.session.headers["Authorization"]


        assert "api_key" not in pet_client.session.headers
        assert "Authorization" not in pet_client.session.headers