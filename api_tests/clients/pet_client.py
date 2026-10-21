import requests
from .base_client import BaseClient

class PetClient(BaseClient):
    def get_pets_by_status(self, status: str = None ):
        """Возвращаем список питомцев с указанным статусом"""
        return self._get("pet/findByStatus", params={"status": status})


    def get_pets_by_id(self, pet_id: int):
        """Получаем ID питомца"""
        return self._get(f"pet/{pet_id}" )

    def create_pets(self, data: dict):
        """Создание питомца с переданными данными POST"""
        return self._post("pet/", json=data)

    def update_pets(self, data: dict):
        """Изменение питомца"""
        return self._put(f"/pet", json=data)

    def delete_pets(self, pet_id):
        """Удаление питомца"""
        return self._delete(f"pet/{pet_id}")