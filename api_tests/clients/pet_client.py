import requests
from .base_client import BaseClient

class PetClient(BaseClient):
    def get_pets_by_status(self, status: str):
        """Возвращаем список питомцев с указанным статусом"""
        return self._get("pet/findByStatus", params={"status": status})


