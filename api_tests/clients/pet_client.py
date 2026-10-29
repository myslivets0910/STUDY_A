import requests
from pygments.lexers import data

from .base_client import BaseClient

class PetClient(BaseClient):
    def get_pet_by_status(self, status: str = None ):
        """Возвращаем список питомцев с указанным статусом"""
        return self._get("pet/findByStatus", params={"status": status})


    def get_pet_by_id(self, pet_id: int):
        """Получаем ID питомца"""
        return self._get(f"pet/{pet_id}" )

    def create_pet(self, data: dict):
        """Создание питомца с переданными данными POST"""
        return self._post("pet/", json=data)

    def update_pet_full(self, data: dict):
        """Изменение питомца"""
        return self._put(f"pet/", json=data)

    def update_pet_patrial(self, pet_id: int, data: dict):
        """Частичное обновление питомца"""
        return self._patch(f"pet/{pet_id}", json=data)

    def delete_pet(self, pet_id):
        """Удаление питомца"""
        return self._delete(f"pet/{pet_id}")

    def set_api_key(self, api_key: str):
        """Устанавливаем API Key в заголовки сессии"""
        return self.session.headers.update({"api_key": api_key})

    def clear_api_key(self):
        """Очищаем API Key после использования"""
        if "api_key" in self.session.headers:
            del self.session.headers["api_key"]