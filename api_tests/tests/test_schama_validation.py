import pytest
from jsonschema import validate, ValidationError

from schemas.pet_sсhema import PET_SCHEMA, PET_LIST_SCHEMA, ERROR_SCHEMA

from api_tests.conftest import pet_client


class TestSchamaValidation:
    """Тесты с валидацией JSON-схемы"""

    def test_get_pet_by_id_matches_schema(self, pet_client):
        """Получение питомца по id возвращает данные, сответствующие схеме"""
        # Получаем список, чтобы взять реальный ID
        list_response = pet_client.get_pet_by_status("available")
        if list_response.status_code != 200 or not list_response.json():
            pytest.skip("Нет доступных питомцев")

        pet_id = list_response.json()[0]["pet_id"]

        # Получение питомца
        response = pet_client.get_pet_by_id(pet_id)
        assert response.status_code == 200

        pet_data = response.json()

        # Валидация схемы
        validate(instance=pet_data, schema=PET_SCHEMA)


    def test_create_pet_response_matches_schemas(self, pet_client):
        """Создание питомца возвращает данные, соответствующие схеме"""
        new_pet_data = {
            "id": 1111,
            "name":"ShemaDog",
            "status":"available"
        }

        response = pet_client.create_pet(new_pet_data)
        assert response.status_code == 200

        create_pet = response.json()

        # Валидируем схему
        validate(instance=create_pet, schema=PET_SCHEMA)
        # Удаляем питомца
        pet_client.delete_pet(create_pet["id"])


    def test_get_pets_by_status_matches_schemas(self, pet_client):
        """Получение спмска питомцев возвращает массив, соот схеме"""
        response = pet_client.get_pets_by_status("available")
        assert response.status_code == 200

        pet_data = response.json()

        validate(instance=pet_data, schema=PET_LIST_SCHEMA)


    def test_error_response_matches_schemas(self, pet_client):
        """Ответ с ошибкой соот схеме"""
        response = pet_client.get_pet_by_id(99999)
        assert response.status_code == 404

        errors_data = response.json()

        validate(instance=errors_data, schema=ERROR_SCHEMA)