import allure
import pytest
from api_client import StellarBurgersAPI
from data.constants import HTTP, ERROR_MESSAGES, API_KEYS


@allure.feature("Получение заказов пользователя")
class TestGetOrders:
    
    @allure.story("Получение заказов авторизованным пользователем")
    @allure.title("Список заказов после создания нового")
    def test_get_orders_authorized(self, created_user, api_client, ingredients_list):
        # Проверка получения списка заказов авторизованным пользователем
        # Pre-condition: создаём заказ для наличия данных
        api_client.create_order(
            ingredients=ingredients_list[:1],
            access_token=created_user["access_token"]
        )
        
        # Получаем список заказов
        response = api_client.get_user_orders(
            access_token=created_user["access_token"]
        )
        
        # Проверка кода ответа
        assert response.status_code == HTTP["OK"]
        
        # Проверка тела ответа
        json_data = response.json()
        assert json_data.get(API_KEYS["success"]) is True
        assert API_KEYS["orders"] in json_data
        assert isinstance(json_data[API_KEYS["orders"]], list)
        
        # Дополнительные проверки структуры
        assert "total" in json_data
        assert "totalToday" in json_data
        assert isinstance(json_data["total"], int)
        assert isinstance(json_data["totalToday"], int)

    @allure.story("Получение заказов без авторизации")
    @allure.title("Попытка получить заказы без токена")
    def test_get_orders_unauthorized(self, api_client):
        # Проверка ошибки при получении заказов без авторизации
        response = api_client.get_user_orders(access_token=None)
        
        # Проверка кода ответа
        assert response.status_code == HTTP["UNAUTHORIZED"]
        
        # Проверка тела ответа
        json_data = response.json()
        assert json_data.get(API_KEYS["success"]) is False
        assert json_data.get(API_KEYS["message"]) == ERROR_MESSAGES["unauthorized"]