import pytest

class TestBearerToken:
    """ Тесты на Bearer token авторизацию"""

    def test_login_returns_token(self, auth_client):
        """Проверка что логин возвращает токен"""

        response = auth_client.login("eve.holt@reqres.in", "cityslicka")

        assert response.status_code == 200
        data = response.json()
        assert "token" in data   # Проверяет что в json есть текст токен
        assert len(data["token"]) > 0 # Проверяет что в значении по ключу токен есть символы, т.е. присутствует


    def test_authenticated_request_with_bearer_token(self, auth_client):
        """Проверка, что запрос с токеном проходит"""
        # Получаем токен
        login_request = auth_client.login("eve.holt@reqres.in", "cityslicka")
        assert login_request.status_code == 200

        token = login_request.json()["token"]

        # Устанавливаем токен в заголовке
        auth_client.set_bearer_token(token)

        # Делаем запрос к защищенному эндпоинту
        user_response = auth_client.get_users()
        assert user_response.status_code == 200

        # Проверяем что ответ содержит данные

        data = user_response.json()
        assert "data" in data
        assert len(data["data"]) > 0

        # Очищаем токен после теста
        auth_client.clear_auth()



    def test_unauthenticated_request_fails(self, auth_client):
        """ПРоверка, что без токена возвращает ошибку (если эндпоинт защищен)"""
        # покажем, что токен не установлен
        auth_client.clear_auth()

        response = auth_client.get_users()
        assert response.status_code == 401


