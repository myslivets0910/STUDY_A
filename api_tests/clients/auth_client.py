from .base_client import BaseClient


class AuthClient(BaseClient):
    """Клиент для демонстрации Bearer Token авторизации"""

    def login(self, email, password):

        payload = {
            "login": email,
            "password": password
        }

        return self._post("/auth/login", json=payload)

    def get_users(self):
        """Запрос к защищенному эндпоинту. Трребует Bearer Token"""
        return self._get("/auth/users")


    def set_bearer_token(self, token):
        """Устанавливаем Bearer token в загаловке сессии"""
        return self.session.headers.update({"Authorization" : f"Bearer {token}"})

    def clear_auth(self):
        """Удаляет токен из загаловков"""
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
