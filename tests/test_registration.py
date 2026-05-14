import allure
import pytest
from api_client import StellarBurgersAPI
from data.constants import HTTP, ERROR_MESSAGES, API_KEYS
from helpers import generate_unique_user


@allure.feature("Регистрация пользователя")
class TestRegistration:
    
    @allure.story("Успешная регистрация")
    @allure.title("Создание уникального пользователя")
    def test_register_unique_user_success(self, api_client, user_cleanup_list):
        # Проверка успешной регистрации нового пользователя
        user = generate_unique_user()
        
        response = api_client.register(**user)
        
        # Проверка кода ответа
        assert response.status_code == HTTP["OK"], (
            f"Ожидался код {HTTP['OK']}, получен {response.status_code}"
        )
        
        # Проверка тела ответа
        json_data = response.json()
        assert json_data.get(API_KEYS["success"]) is True
        assert API_KEYS["access_token"] in json_data
        assert API_KEYS["refresh_token"] in json_data
        assert API_KEYS["user"] in json_data
        
        # Проверка данных пользователя
        user_data = json_data[API_KEYS["user"]]
        assert user_data[API_KEYS["email"]] == user["email"]
        assert user_data[API_KEYS["name"]] == user["name"]
        
        # Добавляем токены в список для очистки
        user_with_tokens = {
            **user,
            "access_token": json_data[API_KEYS["access_token"]],
            "refresh_token": json_data[API_KEYS["refresh_token"]],
        }
        user_cleanup_list.append(user_with_tokens)

    @allure.story("Регистрация существующего пользователя")
    @allure.title("Попытка регистрации с уже занятым email")
    def test_register_existing_user_error(self, created_user, api_client):
        # Проверка ошибки при регистрации пользователя с существующим email
        response = api_client.register(
            email=created_user["email"],
            password=created_user["password"],
            name=created_user["name"]
        )
        
        assert response.status_code == HTTP["FORBIDDEN"]
        json_data = response.json()
        assert json_data.get(API_KEYS["success"]) is False
        assert json_data.get(API_KEYS["message"]) == ERROR_MESSAGES["user_exists"]

    @allure.story("Регистрация без обязательных полей")
    @allure.title("Попытка регистрации с пустым полем {field_name}")
    @pytest.mark.parametrize("empty_field,field_name", [
        ("email", "email"),
        ("password", "password"),
        ("name", "name"),
    ], ids=["empty_email", "empty_password", "empty_name"])
    def test_register_missing_required_field(self, api_client, empty_field, field_name):
        # Проверка ошибки при регистрации с пустым обязательным полем
        # Отправляем пустые строки вместо значений.
        
        # Отправляем пустые строки для указанного поля, остальные заполняем валидными данными
        payload = {
            "email": "" if empty_field == "email" else "test@example.com",
            "password": "" if empty_field == "password" else "Password123!",
            "name": "" if empty_field == "name" else "Test User",
        }
        
        response = api_client.register(**payload)
        
        assert response.status_code == HTTP["FORBIDDEN"]
        json_data = response.json()
        assert json_data.get(API_KEYS["success"]) is False
        assert json_data.get(API_KEYS["message"]) == ERROR_MESSAGES["required_fields"]