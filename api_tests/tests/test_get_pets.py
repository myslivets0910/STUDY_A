import pytest

def test_get_pets_by_available_status(pet_client):
    """Проверка получения списка питомцев со статусом 'available' """

    response = pet_client.get_pets_by_status('available')
    data = response.json()
    # print(response.url)

    assert response.status_code == 200 , "Код не 200"
    assert any(pet.get('status') == "available" for pet in data), "Статуса 'available' нет в ответе"
    assert isinstance(data, list), "Полученные данные список"


def test_get_pets_by_pending_status(pet_client):
    """Проверка получения списка питомцев со статусом 'pending' """

    response = pet_client.get_pets_by_status('pending')
    data = response.json()
    # print(response.url)

    assert response.status_code == 200 , "Код не 200"
    assert any(pet.get('status') == "pending" for pet in data), "Статуса 'pending' нет в ответе"
    assert isinstance(data, list) , "Полученные данные список"


def test_get_pets_by_sold_status(pet_client):
    """ Проверка получения списка питомцев со статусом 'sold' """

    response = pet_client.get_pets_by_status('sold')
    data = response.json()

    assert response.status_code == 200, "Код не 200"
    assert any(pet.get("status") == "sold" for pet in data), "Статуса 'sold' нет в ответе"
    assert isinstance(data, list), "Полученные данные список"


def test_get_pets_available(pet_client):
    """ Проверка на фильтрацию по статусу питомцев в статусе 'available' """

    response = pet_client.get_pets_by_status('available')

    assert response.status_code == 200, f"Ошибка API: {response.status_code}"

    data = response.json()
    for pet in data:
        assert pet["status"] == "available", f' У {data} отсутствует статус'


def test_get_pets_id_and_name(pet_client):
    response = pet_client.get_pets_by_id(1)
    data = response.json()

    assert response.status_code == 200

    # проверка значения
    assert data["id"] == 1, f"ID питомца не совпадает: {data.get['id']}"
    # проверка структуры (ключи)
    assert "id" in data, "В ответе нет ключа id"
    assert "name" in data, "В ответе нет ключа name"


def test_get_pets_empty_status(pet_client):
    response = pet_client.get_pets_by_status()
    assert response.status_code == 400


def test_get_pets_id(pet_client):
    """Проверяем есть ли питомец в списке"""

    response = pet_client.get_pets_by_id(2)
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == 2, "Chester не первый в списке"
    assert data["name"] == "Doggie", "Питомец не Chester"
    # проверяем структуру
    assert "name" in data
    assert "photoUrls" in data
    assert "status" in data


def test_get_pets_invaled_id(pet_client):
    response = pet_client.get_pets_by_id(1000000)
    assert response.status_code == 404

def test_get_pets_invaled_type_id(pet_client):
    response = pet_client.get_pets_by_id("id")
    assert response.status_code == 404



