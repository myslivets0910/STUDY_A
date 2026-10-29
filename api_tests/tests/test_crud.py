
# Отдельные тесты на PUT, PATCH, DELETE.
# Один E2E-тест, который проходит весь жизненный цикл питомца.

import pytest

from api_tests.clients import pet_client


class TestPutPatchDelete:
    """Тесты на обновление и удаление"""

    def test_update_pet_full_put(self, pet_client):
        """PUT - полное обновление"""
        #    1. Cоздаем питомца
        create_data = {
                "id": 555666777,
                "name": "OriginalDog",
                "status": "available"
            }

        create_response = pet_client.create_pet(create_data)
        assert create_response.status_code == 200
        pet_id = create_response.json()["id"]

        # 2. Полное обновление
        update_date = {
            "id": pet_id,
            "name": "UpdatedDog",
            "category": {"id": 1, "name": "Dogs"},
            "photoUrls": [],
            "tags": [{"id": 1, "name": "updated"}],
            "status": "sold"
        }

        put_response = pet_client.update_pet_full(update_date)
        assert put_response.status_code == 200

        # 3. Проверяем что изменения применились

        get_response = pet_client.get_pet_by_id(pet_id)
        assert get_response.status_code == 200

        update_response = get_response.json()
        assert update_response["name"] == "UpdatedDog"
        assert update_response["category"]["id"] == 1
        assert isinstance(update_response["photoUrls"], list)

        # Удаляем для чистоты

        pet_client.delete_pet(pet_id)
        assert pet_client.get_pet_by_id(pet_id).status_code == 404


    def test_update_pet_partial_patch(self, pet_client):
        """PATCH - частичное обновление"""
        # создаем питомца
        create_data = {
            "id": 566666987000011,
            "name": "PatchDog",
            "status": "available"
        }

        create_pet = pet_client.create_pet(create_data)
        assert create_pet.status_code == 200
        pet_id = create_pet.json()["id"]

        # 2. Чвстиное обновление

        patch_response = pet_client.update_pet_patrial(pet_id, {"status": "pending"})
        assert patch_response.status_code == 200

        # 3. Проверяем изменения

        get_response = pet_client.get_pet_by_id(pet_id)
        assert get_response.status_code == 200
        update_pet = get_response.json()
        assert update_pet["name"] == "PatchDog"
        assert update_pet["status"] != "available"
        assert update_pet["status"] != "pending"

        # 4. Удаляем питомца (очистка)
        pet_client.delete_pet(pet_id)
        assert pet_client.get_pet_by_id(pet_id).status_code == 404


class TestFullCRUD:
    """Создать > Получить > Обновить > Удалить > Проверить > Удаление"""
    def test_full_lifecycle(self, pet_client):
        # CREATE
        create_data = {
            "id": 999888777,
            "name": "CRUDDog",
            "status": "available"
        }

        response = pet_client.create_pet(create_data)
        assert response.status_code == 200
        pet_id = response.json()["id"]

        # READ
        get_response = pet_client.get_pet_by_id(pet_id)
        assert get_response.status_code == 200
        assert get_response.json()["name"] == "CRUDDog"

        # UPDATE
        update_data = {
            "id": pet_id,
            "name": "CRUDDogUpdated",
            "category": {"id": 1, "name": "Dogs"},
            "photoUrls": [],
            "tags": [],
            "status": "sold"
        }

        put_response = pet_client.update_pet_full(update_data)
        assert put_response.status_code == 200

        get_response = pet_client.get_pet_by_id(pet_id)
        assert get_response.status_code == 200
        assert get_response.json()["name"] == "CRUDDogUpdated"
        assert get_response.json()["category"]["id"] == 1
        assert isinstance(get_response.json()["photoUrls"], list)
        put_pet_id = get_response.json()["id"]

        # PATCH частичное обновление

        patch_response = pet_client.update_pet_patrial(put_pet_id, {"status": "pending"})
        assert patch_response.status_code == 200

        get_response = pet_client.get_pet_by_id(put_pet_id)
        assert get_response.status_code == 200
        assert get_response.json()["name"] == "CRUDDogUpdated"
        assert get_response.json()["status"] == "pending"


        # DELETE
        delete_pet = pet_client.delete_pet(put_pet_id)
        assert delete_pet.status_code == 200

        # VERIFY DELETION
        get_response = pet_client.get_pet_by_id(put_pet_id)
        assert get_response.status_code == 404
