import pytest

class TestGetPetsCase:
    """Тест для GET-запроса к Pets"""

    def test_get_pets_by_available_status(pet_client):
        """Проверка получения списка питомцев со статусом 'available' """

        response = pet_client.get_pet_by_status('available')
        data = response.json()
        # print(response.url)

        assert response.status_code == 200 , "Код не 200"
        assert any(pet.get('status') == "available" for pet in data), "Статуса 'available' нет в ответе"
        assert isinstance(data, list), "Полученные данные список"


    def test_get_pets_by_pending_status(pet_client):
        """Проверка получения списка питомцев со статусом 'pending' """

        response = pet_client.get_pet_by_status('pending')
        data = response.json()
        # print(response.url)

        assert response.status_code == 200 , "Код не 200"
        assert any(pet.get('status') == "pending" for pet in data), "Статуса 'pending' нет в ответе"
        assert isinstance(data, list) , "Полученные данные список"


    def test_get_pets_by_sold_status(pet_client):
        """ Проверка получения списка питомцев со статусом 'sold' """

        response = pet_client.get_pet_by_status('sold')
        data = response.json()

        assert response.status_code == 200, "Код не 200"
        assert any(pet.get("status") == "sold" for pet in data), "Статуса 'sold' нет в ответе"
        assert isinstance(data, list), "Полученные данные список"


    def test_get_pets_available(pet_client):
        """ Проверка на фильтрацию по статусу питомцев в статусе 'available' """

        response = pet_client.get_pet_by_status('available')

        assert response.status_code == 200, f"Ошибка API: {response.status_code}"

        data = response.json()
        for pet in data:
            assert pet["status"] == "available", f' У {data} отсутствует статус'


    def test_get_pets_id_and_name(pet_client):
        """Падающий тест, так как питомца ID 1 нет в базе"""

        response = pet_client.get_pet_by_id(1)
        data = response.json()

        assert response.status_code == 200

        # проверка значения
        assert data["id"] == 1, f"ID питомца не совпадает: {data.get['id']}"
        # проверка структуры (ключи)
        assert "id" in data, "В ответе нет ключа id"
        assert "name" in data, "В ответе нет ключа name"


    def test_get_pets_empty_status(pet_client):
        """ Негативный тест на отсутствие данных """
        # баговый тест, так как возвращает 200
        response = pet_client.get_pet_by_status()
        assert response.status_code == 400


    def test_get_pets_id(pet_client):
        """Проверяем есть ли питомец в списке"""

        response = pet_client.get_pet_by_id(66)
        data = response.json()

        assert response.status_code == 200
        assert data["id"] == 2, "Chester не первый в списке"
        assert data["name"] == "Doggie", "Питомец не Chester"
        # проверяем структуру
        assert "name" in data
        assert "photoUrls" in data
        assert "status" in data


    def test_get_pets_invalid_id(pet_client):
        """ Негативный тест на некорректные данные ID"""
        response = pet_client.get_pet_by_id(1000000)
        assert response.status_code == 404

    def test_get_pets_invalid_type_id(pet_client):
        """ Негативный тест на некорректные формат данных """
        response = pet_client.get_pet_by_id("id")
        assert response.status_code == 404


class TestPostPetsCase:
    """Тест для POST-запроса к Pets"""

    def test_create_pets_whit_nested_structure(pet_client):
        """Проверка создания питомца с вложенными объектами (category) и массивом (tags))"""
        # Формируем сложный payload
        new_pet_data = {
            "id": 9876543211,
            "name": "ComplexDog",
            "category": {
                "id": 1,
                "name": "Dogs"
            },
            "photoUrls": [
                "https://example.com/photo1.jpg",
                "https://example.com/photo2.jpg"
            ],
            "tags": [
                {"id": 10, "name": "friendly"},
                {"id": 20, "name": "vaccinated"}
            ],
            "status": "available"
        }

        response = pet_client.create_pet(new_pet_data)
        # проверка ответа
        assert response.status_code == 200

        created_pet = response.json()
        # проверяем что сервер вернул нащи данные
        assert created_pet["id"] == 9876543211 # проверили что ID соответствует
        assert created_pet["name"] == "ComplexDog" # проверили что имя соответствует
        assert created_pet["status"] == "available" # проверили что статус соответствует

        # проверяем вложенный словарь
        assert "category" in created_pet # проверили что ключ категории есть в ответе
        assert created_pet["category"]["name"] == "Dogs" # проверили что в словаре категорий по ключу name именно Dogs

        # проверяем список
        assert "tags" in created_pet # проверили что есть ключ тэгс в ответе
        assert len(created_pet["tags"]) == 2 # проверили что в списке тэгс 2 записи
        assert created_pet["tags"][0]['name'] == "friendly" # проверили что в первой записи списка тэгы есть ключ name со значение friendly


    def test_created_pet_min_characteristics(pet_client):
        """Проверяем создание с минимальным необходимым набором"""

        minimal_data = {
            "id": 111222333,
            "name": "MinimalCat",
            "status": "pending"
        }

        response = pet_client.create_pet(minimal_data)
        assert response.status_code == 200

        created_pet = response.json()
        assert created_pet["id"] == 111222333 # проверили что ID соответствует
        assert created_pet["name"] == "MinimalCat" # проверили что имя соответствует
        assert created_pet["status"] == "pending" # проверили что статус соответствует