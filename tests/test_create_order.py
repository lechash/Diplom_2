import allure
import pytest
from api_client import StellarBurgersAPI
from data.constants import HTTP, ERROR_MESSAGES, API_KEYS


@allure.feature("Создание заказа")
class TestOrderCreation:
    
    @allure.story("Успешное создание заказа с авторизацией")
    @allure.title("Заказ с валидными ингредиентами")
    def test_create_order_authorized_with_ingredients(self, created_user, api_client, ingredients_list):
        # Проверка создания заказа авторизованным пользователем
        selected = ingredients_list[:2]
        
        response = api_client.create_order(
            ingredients=selected,
            access_token=created_user["access_token"]
        )
        
        assert response.status_code == HTTP["OK"]
        
        json_data = response.json()
        assert json_data.get(API_KEYS["success"]) is True
        assert API_KEYS["order"] in json_data
        
        order = json_data[API_KEYS["order"]]
        assert API_KEYS["number"] in order
        assert isinstance(order[API_KEYS["number"]], int)
        assert order[API_KEYS["number"]] > 0

    @allure.story("Создание заказа без авторизации")
    @allure.title("Создание заказа без токена (ожидаем 401 по документации)")
    @pytest.mark.xfail(reason="API возвращает 200 вместо 401, см. документацию", strict=False)
    def test_create_order_unauthorized_expected_401(self, api_client, ingredients_list):
        # Проверка создания заказа без авторизации
        # Ожидаем 401 Unauthorized согласно документации API:
        # "Только авторизованные пользователи могут делать заказы"
        # "Если выполнить запрос без авторизации, вернется код ответа 401 Unauthorized"
        # 
        # ⚠️ ВНИМАНИЕ: Фактически сервер возвращает 200 OK для неавторизованных запросов.
        # Этот тест помечен как xfail и будет "падать" (ожидаемо), пока поведение API не будет приведено в соответствие с документацией.
        
        response = api_client.create_order(
            ingredients=ingredients_list[:2],
            access_token=None
        )
        
        # Ожидаем код ответа согласно документации
        assert response.status_code == HTTP["UNAUTHORIZED"], (
            f"Согласно документации, ожидается {HTTP['UNAUTHORIZED']}, "
            f"но сервер вернул {response.status_code}. "
            f"Тело ответа: {response.text}"
        )
        
        # Ожидаем сообщение об ошибке согласно документации
        json_data = response.json()
        assert json_data.get(API_KEYS["success"]) is False
        assert json_data.get(API_KEYS["message"]) == ERROR_MESSAGES["unauthorized"]

    @allure.story("Создание заказа без авторизации, версия если 200 это ОК")
    @allure.title("Создание заказа без токена (разрешено API)")
    def test_create_order_unauthorized(self, api_client, ingredients_list):
        # Фактически API принимает запросы на создание заказа без токена и возвращает 200.
        
        response = api_client.create_order(
            ingredients=ingredients_list[:2],
            access_token=None
        )
        
        # API фактически возвращает 200 для неавторизованных запросов
        assert response.status_code == HTTP["OK"]
        
        json_data = response.json()
        assert json_data.get(API_KEYS["success"]) is True
        assert API_KEYS["order"] in json_data
        assert API_KEYS["number"] in json_data[API_KEYS["order"]]

    @allure.story("Создание заказа без ингредиентов")
    @allure.title("Попытка создать заказ с пустым списком ингредиентов")
    @pytest.mark.parametrize("with_auth", [True, False], ids=["authorized", "unauthorized"])
    def test_create_order_empty_ingredients(self, created_user, api_client, with_auth):
        # Проверка ошибки при создании заказа без ингредиентов
        access_token = created_user["access_token"] if with_auth else None
        
        response = api_client.create_order(
            ingredients=[],
            access_token=access_token
        )
        
        assert response.status_code == HTTP["BAD_REQUEST"]
        
        json_data = response.json()
        assert json_data.get(API_KEYS["success"]) is False
        assert json_data.get(API_KEYS["message"]) == ERROR_MESSAGES["ingredients_required"]

    @allure.story("Создание заказа с неверными данными")
    @allure.title("Попытка создать заказ с невалидным хешем ингредиента")
    def test_create_order_invalid_ingredient_hash(self, created_user, api_client):
        # Проверка обработки запроса с несуществующим ID ингредиента
        invalid_ids = ["invalid_hash_123", "fake_ingredient_id"]
        
        response = api_client.create_order(
            ingredients=invalid_ids,
            access_token=created_user["access_token"]
        )
        
        # API возвращает 500 при неверном хеше (согласно документации)
        assert response.status_code == HTTP["INTERNAL_ERROR"]