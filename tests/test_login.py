import allure
import pytest
from api_client import StellarBurgersAPI
from data.constants import HTTP, ERROR_MESSAGES, API_KEYS


@allure.feature("Авторизация пользователя")
class TestLogin:
    
    @allure.story("Успешная авторизация")
    @allure.title("Вход под существующим пользователем")
    def test_login_success(self, created_user, api_client):
        # Проверка успешного входа с валидными учётными данными
        response = api_client.login(
            email=created_user["email"],
            password=created_user["password"]
        )
        
        assert response.status_code == HTTP["OK"]
        json_data = response.json()
        
        assert json_data.get(API_KEYS["success"]) is True
        assert API_KEYS["access_token"] in json_data
        assert API_KEYS["refresh_token"] in json_data
        assert API_KEYS["user"] in json_data
        
        # Проверка данных пользователя в ответе
        user_data = json_data[API_KEYS["user"]]
        assert user_data[API_KEYS["email"]] == created_user["email"]
        assert user_data[API_KEYS["name"]] == created_user["name"]

    @allure.story("Неверная авторизация")
    @allure.title("Вход с неверным email")
    def test_login_invalid_email(self, created_user, api_client):
        # Проверка ошибки при входе с несуществующим email
        response = api_client.login(
            email="nonexistent@test.ru",
            password=created_user["password"]
        )
        
        assert response.status_code == HTTP["UNAUTHORIZED"]
        json_data = response.json()
        assert json_data.get(API_KEYS["success"]) is False
        assert json_data.get(API_KEYS["message"]) == ERROR_MESSAGES["invalid_credentials"]

    @allure.story("Неверная авторизация")
    @allure.title("Вход с неверным паролем")
    def test_login_invalid_password(self, created_user, api_client):
        # Проверка ошибки при входе с неверным паролем
        response = api_client.login(
            email=created_user["email"],
            password="WrongPassword123!"
        )
        
        assert response.status_code == HTTP["UNAUTHORIZED"]
        json_data = response.json()
        assert json_data.get(API_KEYS["success"]) is False
        assert json_data.get(API_KEYS["message"]) == ERROR_MESSAGES["invalid_credentials"]

    @allure.story("Неверная авторизация")
    @allure.title("Вход с пустыми учётными данными")
    def test_login_empty_credentials(self, api_client):
        # Проверка ошибки при входе без указания логина/пароля
        response = api_client.login(email="", password="")
        
        assert response.status_code == HTTP["UNAUTHORIZED"]
        json_data = response.json()
        assert json_data.get(API_KEYS["success"]) is False
        assert json_data.get(API_KEYS["message"]) == ERROR_MESSAGES["invalid_credentials"]