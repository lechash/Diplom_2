import allure
import pytest
from api_client import StellarBurgersAPI
from data.constants import HTTP, ERROR_MESSAGES, API_KEYS
from helpers import generate_unique_user


@allure.feature("Обновление данных пользователя")
class TestUserUpdate:
    
    @allure.story("Успешное обновление с авторизацией")
    @allure.title("Изменение имени пользователя")
    def test_update_user_name_authorized(self, created_user, api_client):
        # Проверка успешного обновления имени
        new_name = "Updated Name"
        response = api_client.update_user(
            access_token=created_user["access_token"],
            name=new_name
        )
        
        assert response.status_code == HTTP["OK"]
        json_data = response.json()
        assert json_data.get(API_KEYS["success"]) is True
        assert json_data[API_KEYS["user"]][API_KEYS["name"]] == new_name

    @allure.story("Успешное обновление с авторизацией")
    @allure.title("Изменение email пользователя")
    def test_update_user_email_authorized(self, created_user, api_client):
        # Проверка успешного обновления email
        # Генерируем уникальный email для обновления
        import uuid
        new_email = f"updated_{uuid.uuid4().hex[:8]}@test.ru"
        
        response = api_client.update_user(
            access_token=created_user["access_token"],
            email=new_email
        )
        
        assert response.status_code == HTTP["OK"]
        json_data = response.json()
        assert json_data.get(API_KEYS["success"]) is True
        assert json_data[API_KEYS["user"]][API_KEYS["email"]] == new_email

    @allure.story("Успешное обновление с авторизацией")
    @allure.title("Изменение пароля пользователя")
    def test_update_user_password_authorized(self, created_user, api_client):
        # Проверка успешного обновления пароля
        new_password = "NewSecurePass123!"
        
        response = api_client.update_user(
            access_token=created_user["access_token"],
            password=new_password
        )
        
        assert response.status_code == HTTP["OK"]
        json_data = response.json()
        assert json_data.get(API_KEYS["success"]) is True
        # Сервер не возвращает пароль, проверяем только успешность
        assert API_KEYS["user"] in json_data

    @allure.story("Обновление без авторизации")
    @allure.title("Попытка изменения имени без токена")
    def test_update_user_name_unauthorized(self, api_client, created_user):
        # Проверка ошибки при обновлении имени без авторизации
        response = api_client.update_user(
            access_token=None,
            name="Hacker Name"
        )
        
        assert response.status_code == HTTP["UNAUTHORIZED"]
        json_data = response.json()
        assert json_data.get(API_KEYS["success"]) is False
        assert json_data.get(API_KEYS["message"]) == ERROR_MESSAGES["unauthorized"]

    @allure.story("Обновление без авторизации")
    @allure.title("Попытка изменения email без токена")
    def test_update_user_email_unauthorized(self, api_client, created_user):
        # Проверка ошибки при обновлении email без авторизации
        response = api_client.update_user(
            access_token=None,
            email="hacker@test.ru"
        )
        
        assert response.status_code == HTTP["UNAUTHORIZED"]
        json_data = response.json()
        assert json_data.get(API_KEYS["success"]) is False
        assert json_data.get(API_KEYS["message"]) == ERROR_MESSAGES["unauthorized"]

    @allure.story("Обновление без авторизации")
    @allure.title("Попытка изменения пароля без токена")
    def test_update_user_password_unauthorized(self, api_client, created_user):
        # Проверка ошибки при обновлении пароля без авторизации
        response = api_client.update_user(
            access_token=None,
            password="HackedPass123!"
        )
        
        assert response.status_code == HTTP["UNAUTHORIZED"]
        json_data = response.json()
        assert json_data.get(API_KEYS["success"]) is False
        assert json_data.get(API_KEYS["message"]) == ERROR_MESSAGES["unauthorized"]

    @allure.story("Обновление с занятым email")
    @allure.title("Попытка установить уже существующий email")
    def test_update_user_duplicate_email(self, api_client, created_user):
        # Проверка ошибки при установке email, который уже используется
        # Создаём второго пользователя для занятия email
        other_user = generate_unique_user()
        api_client.register(**other_user)
        
        # Пытаемся установить занятый email первому пользователю
        response = api_client.update_user(
            access_token=created_user["access_token"],
            email=other_user["email"]
        )
        
        assert response.status_code == HTTP["FORBIDDEN"]
        json_data = response.json()
        assert json_data.get(API_KEYS["success"]) is False
        assert json_data.get(API_KEYS["message"]) == ERROR_MESSAGES["email_exists"]