import pytest

def test_get_pets_by_available_status(pet_client):
    """Проверка получения списка питомцев со статусом 'available' """

    response = pet_client.get_pets_by_status('available')
    data = response.json()
    # print(response.url)

    assert response.status_code == 200 , "Код не 200"
    assert any(pet.get('status') == "available" for pet in data), "Статуса 'available' нет в ответе"